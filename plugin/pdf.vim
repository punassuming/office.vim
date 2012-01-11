if !isdirectory(expand('$PDFTKHOME'))
    let $PDFTKHOME=expand('$HOME/.vim/tools/')
endif
" If the directory exists, create the autocommands
if isdirectory(expand('$PDFTKHOME'))
    autocmd BufReadPre *.pdf set ro
    autocmd BufReadPre *.pdf set hlsearch!
    autocmd BufReadPre *.pdf set wrap
    " This prevents the hit-enter prompt and allows me to operate
    " without anitword being in the system path
    " exec 'autocmd BufReadPost *.pdf %! '.expand($PDFTKHOME).'pdftotext -layout "%" -'
    exec 'autocmd BufReadPost *.pdf %! '.expand($PDFTKHOME).'pdftotext -nopgbrk -layout -q -eol unix "%" -'
    exec 'autocmd BufReadPost *.pdf :set nolist'
    exec 'autocmd BufReadPost *.pdf :g/^$/d'
    exec 'autocmd BufReadPost *.pdf :%s/^\s*\d\+$//'
    " exec 'autocmd BufReadPost *.pdf :g/\n^$/normal! vipJ'
endif
