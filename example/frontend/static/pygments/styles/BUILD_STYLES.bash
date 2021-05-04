#!/bin/bash

for style in 'autumn' 'borland' 'bw' 'colorful' 'default' 'emacs' 'friendly' 'fruity' 'igor' 'manni' 'monokai' 'murphy' 'native' 'paraiso-dark' 'paraiso-light' 'pastie' 'perldoc' 'rrt' 'tango' 'trac' 'vim' 'vs' 'xcode'
do
    echo $style"..."
    pygmentize -S $style -f html > $style.css
done
