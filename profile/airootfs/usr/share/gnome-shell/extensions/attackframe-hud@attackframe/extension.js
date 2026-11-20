// AttackFrame HUD — top-bar operator readout:  ◢ LAN 192.168.1.20 │ VPN 10.10.14.3 │ TGT 10.10.11.5
// The target is shared with the shell via ~/.config/attackframe/target (`target <ip>` in zsh).
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import GObject from 'gi://GObject';
import St from 'gi://St';
import Clutter from 'gi://Clutter';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const TARGET_FILE = GLib.build_filenamev([GLib.get_user_config_dir(), 'attackframe', 'target']);
const VPN_RE = /^(tun|tap|wg|ppp|tailscale)/;
const SKIP_RE = /^(lo|docker|podman|veth|br-|virbr)/;
const IP_RE = /^[0-9a-fA-F.:/-]+$|^[a-zA-Z0-9.-]+$/;
const C = {cyan: '#00f0ff', mag: '#ff2bd6', yel: '#f5ff3b', dim: '#3a4660', red: '#ff3355'};

function readTarget() {
    try {
        const [ok, bytes] = GLib.file_get_contents(TARGET_FILE);
        if (ok)
            return new TextDecoder().decode(bytes).trim();
    } catch (_e) {}
    return '';
}

function writeTarget(value) {
    GLib.mkdir_with_parents(GLib.path_get_dirname(TARGET_FILE), 0o755);
    GLib.file_set_contents(TARGET_FILE, value ? `${value}\n` : '');
}

function run(argv) {
    return new Promise(resolve => {
        try {
            const proc = Gio.Subprocess.new(argv,
                Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_SILENCE);
            proc.communicate_utf8_async(null, null, (p, res) => {
                try {
                    const [, out] = p.communicate_utf8_finish(res);
                    resolve(out ?? '');
                } catch (_e) {
                    resolve('');
                }
            });
        } catch (_e) {
            resolve('');
        }
    });
}

// `ip -4 -o addr show` → [{iface, ip}]
function parseAddrs(out) {
    const list = [];
    for (const line of out.split('\n')) {
        const m = line.match(/^\d+:\s+(\S+)\s+inet\s+([\d.]+)\//);
        if (m && !SKIP_RE.test(m[1]))
            list.push({iface: m[1], ip: m[2]});
    }
    return list;
}

const esc = s => GLib.markup_escape_text(s, -1);

const Hud = GObject.registerClass(
class AttackFrameHud extends PanelMenu.Button {
    _init() {
        super._init(0.0, 'AttackFrame HUD');
        this._lan = this._vpn = this._tgt = '';

        this._label = new St.Label({
            style_class: 'af-hud-label',
            y_align: Clutter.ActorAlign.CENTER,
        });
        this.add_child(this._label);

        const copy = (title, getter) => {
            const item = new PopupMenu.PopupMenuItem(title);
            item.connect('activate', () => {
                const v = getter();
                if (v)
                    St.Clipboard.get_default().set_text(St.ClipboardType.CLIPBOARD, v);
            });
            this.menu.addMenuItem(item);
            return item;
        };
        this._lanItem = copy('Copy LAN IP', () => this._lan);
        this._vpnItem = copy('Copy VPN IP', () => this._vpn);
        this._tgtItem = copy('Copy target', () => this._tgt);
        this.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

        const setFromClip = new PopupMenu.PopupMenuItem('Set target from clipboard');
        setFromClip.connect('activate', () => {
            St.Clipboard.get_default().get_text(St.ClipboardType.CLIPBOARD, (_cb, text) => {
                const t = (text ?? '').trim();
                if (t && t.length < 256 && IP_RE.test(t))
                    writeTarget(t);
            });
        });
        this.menu.addMenuItem(setFromClip);

        const clear = new PopupMenu.PopupMenuItem('Clear target');
        clear.connect('activate', () => writeTarget(''));
        this.menu.addMenuItem(clear);

        this._monitor = Gio.File.new_for_path(TARGET_FILE)
            .monitor_file(Gio.FileMonitorFlags.NONE, null);
        this._monitorId = this._monitor.connect('changed', () => this._refresh());
        this._timer = GLib.timeout_add_seconds(GLib.PRIORITY_DEFAULT, 5, () => {
            this._refresh();
            return GLib.SOURCE_CONTINUE;
        });
        this._refresh();
    }

    async _refresh() {
        const addrs = parseAddrs(await run(['ip', '-4', '-o', 'addr', 'show']));
        if (this._destroyed)
            return;
        const vpn = addrs.find(a => VPN_RE.test(a.iface));
        const lan = addrs.find(a => !VPN_RE.test(a.iface));
        this._lan = lan?.ip ?? '';
        this._vpn = vpn?.ip ?? '';
        this._tgt = readTarget();

        const seg = (k, v, color) =>
            `<span foreground="${C.dim}">${k}</span> <span foreground="${v ? color : C.red}">${esc(v || '--')}</span>`;
        const sep = `<span foreground="${C.dim}"> │ </span>`;
        this._label.clutter_text.set_markup(
            `<span foreground="${C.mag}">◢</span> ${seg('LAN', this._lan, C.cyan)}${sep}` +
            `${seg('VPN', this._vpn, C.yel)}${sep}${seg('TGT', this._tgt, C.mag)}`);

        this._lanItem.label.text = `Copy LAN IP   ${this._lan || '--'}${lan ? `  (${lan.iface})` : ''}`;
        this._vpnItem.label.text = `Copy VPN IP   ${this._vpn || '--'}${vpn ? `  (${vpn.iface})` : ''}`;
        this._tgtItem.label.text = `Copy target   ${this._tgt || '--'}`;
    }

    destroy() {
        this._destroyed = true;
        if (this._timer) {
            GLib.source_remove(this._timer);
            this._timer = 0;
        }
        if (this._monitor) {
            this._monitor.disconnect(this._monitorId);
            this._monitor.cancel();
            this._monitor = null;
        }
        super.destroy();
    }
});

export default class AttackFrameHudExtension extends Extension {
    enable() {
        this._hud = new Hud();
        Main.panel.addToStatusArea(this.uuid, this._hud, 1, 'left');
    }

    disable() {
        this._hud?.destroy();
        this._hud = null;
    }
}
