"Making and Modifying Documents

    "Just download python xls.
    "Use pip or easy_install to fetch the xlsx2csv script:
    "       https://github.com/dilshod/xlsx2csv .

if !isdirectory(expand('$XLS'))
    let $XLS=expand('$HOME/.vim/tools/')
endif
" If the directory exists, create the autocommands
if isdirectory(expand('$XLS'))
    autocmd BufReadPre *.xlsx let g:csv_delimiter = ";"
    autocmd BufReadPre *.xlsx set ro | setf csv
    autocmd BufReadPre *.xlsx set hlsearch!
    " This prevents the hit-enter prompt and allows me to operate
    " without xls being in the system path
    exec 'autocmd BufReadPost *.xlsx %! python '.expand($XLS).'xlsx2csv.py "%"'
    autocmd BufReadPost *.xlsx redraw
endif
