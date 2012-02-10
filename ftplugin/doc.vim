if !isdirectory(expand('$ANTIWORDHOME'))
    let $ANTIWORDHOME=expand('$HOME/.vim/tools/antiword')
endif

" If the directory exists, create the autocommands
" autocmd BufReadPre *.doc set ro
augroup ft_antiword
    au!
    autocmd BufReadPre *.doc set hlsearch!
    " This prevents the hit-enter prompt and allows me to operate
    " TODO implement this as ftplugin
    " without anitword being in the system path
    " exec 'autocmd BufReadPost *.doc %!'.expand($ANTIWORDHOME).'/antiword -i 1 -s -f "%"'
    autocmd BufReadCmd *.doc if isdirectory(expand("$ANTIWORDHOME")) | call WordFilter() | endif
    " exec 'autocmd BufReadPost *.doc %!'.expand($ANTIWORDHOME).'/antiword -f "%"'
augroup END

function! WordFilter()
    setlocal noreadonly modifiable
    exec "%!" . expand("$ANTIWORDHOME") . "/antiword -i 1 -s -f %:p"
    " silent %s/^\s\+\.\s\+/ â¢ /
    setlocal nolist wrap
    setlocal readonly nomodifiable
endfunction
