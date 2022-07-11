# DVERTKEY-NG

A script that generates AutoHotKey scripts and executables to send the qwerty equivalent of a dvorak key when the ctrl,
alt, and/or win keys are also pressed. 

## Downloads

Find pre-generated scripts and compiled binaries in the releases section

## Inspirations and thanks

This project was inspired by and uses code from https://github.com/imathew/dvertkey, automating the generation of
the AHK scripts and their conversion into Windows executables. This project attempts to build on the layout
detection code so that no script manipulations are needed, by automatic the process of layout detection. It also
attempts to "future-proof" the generated scripts by generating mappings for _all_ number and letter keys on the 
keyboard.

The "D" key icon is taken from https://www.techonthenet.com/clipart/keyboard/letter_d.php

## Why

Many common hotkeys are defined based on their useful position on the qwerty keyboard, such as cut-copy-paste next to 
each other in the bottom left. It's handy to retain this consistent functionality while using dvorak for regular typing, 
but while this option is available out-of-the-box in macOS, it's not in Windows.

For an explanation of why AutoHotKey is used for key remapping, see
https://github.com/imathew/dvertkey/blob/master/README.md#why-autohotkey

## Script usage

The script depends only on the Python stdlib and Win32 API. To generate a binary for your Dvorak keyboard layout

    git clone dvertkey-ng
    cd dvertkey-ng
    python dvertkey.py --generateexe

Make sure that your Dvorak layout is active in Windows when running the script, as the script will automatically 
detect your current layout and generate an AHK script that will remap the keys of your current layout. You will
find the generated files in the out directory. The names of the files will contain the ID of the layout that will
be remapped. Known IDs:
 - 04090409 - Windows 11 US QWERTY. This is the normal QWERTY layout that should not be remapped (make sure that you have Dvorak layout active when running the script)
 - F0020409 - Windows 11 US Dvorak. This is the default Dvorak layout that comes with Windows 11. Pre-generated files for this layout are provided on the releases page.

For executable generation, the AutoHotKey compiler must be located in "C:\Program Files\AutoHotkey\Compiler\", which
is the default when installing AutoHotKey

## Generated executable usage

Run the generated executable, and it will automatically remap the keys when your Dvorak layout is active. You
can set it up start automatically if you want.

## Pre-generated files

Pre-generated AHK and binary files are provided in the releases section of this repository. The mappings used and
the layout ID are for layout F0020409, that is, the US English Dvorak that comes with Windows 11.

## Future work

1. Add more mappings, and add the ability for the script to automatically detect which mapping to use based on the detected layout.
