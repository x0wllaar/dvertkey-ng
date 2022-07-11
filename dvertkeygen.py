import argparse
import ctypes
import os
import csv
import subprocess
import pathlib

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_MAPPING_PATH = os.path.join(SCRIPT_DIR, "mappings", "mapping_default.csv")
ICON_FILE_PATH = os.path.join(SCRIPT_DIR, "letter_d.ico")
AHK_COMPILER_PATH = """C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"""

WIN32_GETKEYBOARDLAYOUT = ctypes.windll.user32.GetKeyboardLayout

AHK_PRELUDE = """
#NoEnv
#UseHook
SendMode Input

get_layout() {
  SetFormat, Integer, H
  WinGet, WinID,, A
  threadID := DllCall("GetWindowThreadProcessId", "UInt", WinID, "UInt", 0)
  localeID := DllCall("GetKeyboardLayout", "UInt", threadID, "UInt")
  return localeID
}

"""


def get_current_keyboard_layout():
    keyboard_layout_int = WIN32_GETKEYBOARDLAYOUT(0)
    keyboard_layout_uint = ctypes.c_ulong(keyboard_layout_int)
    return keyboard_layout_uint.value


def get_current_keyboard_layout_string():
    kbdl = get_current_keyboard_layout()
    kbdl_str = hex(kbdl).upper().replace("0X", "")
    kbdl_str = "0" * (8 - len(kbdl_str)) + kbdl_str
    return "0x" + kbdl_str


parser = argparse.ArgumentParser(description="Generates dvertkey AHK mapping scripts from keyboard mappings")
parser.add_argument("--mapping",
                    type=str,
                    required=False,
                    default=os.path.join(
                        SCRIPT_DIR,
                        "mappings",
                        "mapping_" + get_current_keyboard_layout_string().replace("0x", "") + ".csv"),
                    help="Path to the CSV file containing QWERTY->Dvorak mappings")
parser.add_argument("--layoutid",
                    type=str,
                    required=False,
                    default=get_current_keyboard_layout_string(),
                    help="ID of the Dvorak layout in hex as returned by GetKeyboardLayout")
parser.add_argument("--output",
                    type=str,
                    required=False,
                    default=os.path.join(
                        SCRIPT_DIR,
                        "out",
                        "ahk",
                        "dvertkey_" + get_current_keyboard_layout_string().replace("0x", "")) + ".ahk",
                    help="Where to store the generated AHK file")
parser.add_argument("--exeoutput",
                    type=str,
                    required=False,
                    default=os.path.join(
                        SCRIPT_DIR,
                        "out",
                        "exe",
                        "dvertkey_" + get_current_keyboard_layout_string().replace("0x", "")) + ".exe",
                    help="Where to store the generated executable file")
parser.add_argument("--generateexe",
                    action="store_true",
                    help="Generate executable file")
parser.add_argument("--compressexe",
                    action="store_true",
                    help="Compress generated executable with UPX")


def main():
    args = parser.parse_args()

    mapping_path = args.mapping
    if not (os.path.exists(mapping_path) and os.path.isfile(mapping_path)):
        mapping_path = DEFAULT_MAPPING_PATH
    mapping = {}
    with open(mapping_path, "r", encoding="utf-8") as mappingf:
        reader = csv.DictReader(mappingf)
        for row in reader:
            mapping[row["QWERTY"]] = row["ALT"]

    pathlib.Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)
    with open(args.output, "w+", encoding="utf-8") as hotkeyf:
        print(AHK_PRELUDE, file=hotkeyf, flush=True)
        print(f"alternative := {args.layoutid}\n", file=hotkeyf, flush=True)
        print("#If get_layout() = alternative\n", file=hotkeyf, flush=True)
        for qwerty, alt in mapping.items():
            if qwerty != alt:
                print(f"*^{alt}::", file=hotkeyf, flush=True)
                print(f"*!{alt}::", file=hotkeyf, flush=True)
                print(f"*#{alt}::Send {{Blind}}{qwerty}\n", file=hotkeyf, flush=True)

    if args.generateexe:
        pathlib.Path(os.path.dirname(args.exeoutput)).mkdir(parents=True, exist_ok=True)
        res = subprocess.call(
            args=[AHK_COMPILER_PATH,
                  "/in", args.output,
                  "/icon", ICON_FILE_PATH,
                  "/compress", "2" if args.compressexe else "0",
                  "/out", args.exeoutput],
            cwd=os.path.dirname(AHK_COMPILER_PATH)
        )
        if res != 0:
            raise RuntimeError(f"Bad return code from AHK compiler: {res}")


if __name__ == '__main__':
    main()
