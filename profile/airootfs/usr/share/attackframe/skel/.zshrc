# ── AttackFrame OS zsh ─────────────────────────────────────────────────────
HISTFILE=~/.zsh_history; HISTSIZE=50000; SAVEHIST=50000
setopt hist_ignore_dups share_history auto_cd interactive_comments prompt_subst
autoload -Uz compinit && compinit -d ~/.cache/zcompdump
zstyle ':completion:*' menu select
bindkey -e

for p in /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh \
         /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh; do
  [[ -r $p ]] && source $p
done
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#3a4660'
[[ -r /usr/share/fzf/key-bindings.zsh ]] && source /usr/share/fzf/key-bindings.zsh
export FZF_DEFAULT_OPTS='--color=bg+:#0b0f1a,fg:#c8f7ff,hl:#ff2bd6,fg+:#00f0ff,hl+:#ff2bd6,pointer:#ff2bd6,prompt:#00f0ff,border:#1a2233 --border'
export PATH=$HOME/.local/bin:$PATH
export EDITOR=nvim

# ── ops helpers ──────────────────────────────────────────────────────────────
AF_TARGET_FILE=${XDG_CONFIG_HOME:-$HOME/.config}/attackframe/target
target() {   # target 10.10.11.5  |  target (show)  |  target -c (clear)
  mkdir -p ${AF_TARGET_FILE:h}
  case $1 in
    '') cat $AF_TARGET_FILE 2>/dev/null ;;
    -c) : > $AF_TARGET_FILE ;;
    *)  print -r -- $1 > $AF_TARGET_FILE ;;
  esac
}
lhost() {    # VPN address if a tunnel is up, otherwise the LAN address
  local v=$(ip -4 -o addr show 2>/dev/null | awk '$2 ~ /^(tun|tap|wg|ppp)/{split($4,a,"/");print a[1];exit}')
  [[ -n $v ]] && { print $v; return }
  ip -4 -o addr show scope global 2>/dev/null | awk '$2 !~ /^(docker|podman|veth|br-)/{split($4,a,"/");print a[1];exit}'
}
precmd() { TGT=$(cat $AF_TARGET_FILE 2>/dev/null); export TGT LHOST=$(lhost) }

alias ls='eza --group-directories-first --icons' ll='eza -la --git --icons' cat='bat -pp'
alias serve='python -m http.server' ports='ss -tulpn' myip='curl -s https://ifconfig.me; echo'
alias arsenal='attackframe-arsenal' nse='ls /usr/share/nmap/scripts | grep'
alias scan='sudo nmap -sC -sV -oA scan-$TGT $TGT' fullscan='sudo nmap -p- --min-rate 5000 -oA full-$TGT $TGT'

# ── prompt ───────────────────────────────────────────────────────────────────
# Arch's grml-zsh-config redraws its own prompt on every precmd; switch it off.
(( $+functions[prompt] )) && prompt off 2>/dev/null
setopt prompt_subst   # `prompt off` resets it
#  ┌─[ghost@attackframe]─[~/loot]─[tgt 10.10.11.5]
#  └──╼ ▶
_af_tgt() { [[ -n $TGT ]] && print -n "─[%F{#ff2bd6}tgt $TGT%F{#00f0ff}]" }
_af_err() { print -n "%(?..%F{#ff3355}✗ %?%F{#00f0ff} )" }
PROMPT=$'%F{#00f0ff}┌─[%F{#c8f7ff}%n%F{#ff2bd6}@%F{#c8f7ff}%m%F{#00f0ff}]─[%F{#f5ff3b}%~%F{#00f0ff}]$(_af_tgt)\n%F{#00f0ff}└──╼ $(_af_err)%F{#ff2bd6}▶%f '
RPROMPT='%F{#3a4660}$LHOST %*%f'

[[ -o interactive && -z $AF_QUIET && $SHLVL -le 2 ]] && af-banner
