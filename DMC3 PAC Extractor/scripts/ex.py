# PAC Extractor (Python 3 Refactored)
# Originally coded by James, updated by Dante to use python 3.12

import sys
import os
from struct import unpack
import time

time_start = time.time()
gotta_go_deep = 0

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    result = []
    temp = ""
    for char in text:
        if not temp:
            temp += char
        elif char.isdigit() == temp[-1].isdigit():
            temp += char
        else:
            result.append(atoi(temp))
            temp = char
    if temp:
        result.append(atoi(temp))
    return result

def getFiles(data):
    num_files = unpack("<I", data[4:8])[0]
    offset = 8
    offsets = []
    
    for i in range(num_files):
        file_offset = unpack("<I", data[offset:offset+4])[0]
        if file_offset != 0 and file_offset not in offsets:
            offsets.append(file_offset)
        offset += 4
    return offsets

def getType(data):
    try:
        if data[:4] == b"MOD " or data[:3] == b"MOD":
            suf = "mod"
        elif data[:4] == b"DDS " or data[:3] == b"DDS":
            suf = "dds"
        elif data[:4] == b"SHW " or data[:3] == b"SHW":
            suf = "shw"
        elif data[:3] == b"MOT" or data[:8] == b"P\x00\x00\x00MOT\x00":
            suf = "mot"
        elif data[:3] == b"PAC" or data[:4] == b"PNST":
            suf = "pac"
        elif data[:4] == b"OggS" or data[:3] == b"Ogg":
            suf = "ogg"
        elif data[:4] == b"BM6\x00" or data[:3] == b"BM6":
            suf = "bm6"
        elif data[:4] == b"\x00\x00\x01\xba":
            suf = "mpg"
        elif data[:4] == b"LIG2":
            suf = "lig"
        elif data[:3] == b"SEF":
            suf = "sef"
        elif data[:3] == b"CAM":
            suf = "cam"
        elif data[:3] == b"EVE":
            suf = "eve"
        elif data[:3] == b"POS":
            suf = "pos"
        elif data[:4] == b"\xef\xbb\xbf#":
            suf = "txt"
        elif data[:4] == b"\x00\x00\x00\x00":
            suf = "bd"
        elif data[:4] == b"\x00\x00\x01\x00":
            suf = "ico"
        elif data[:4] == b"dbsT" or data[:4] == b"dbst":
            suf = "tsb"
        elif data[:2] == b"# ":
            suf = "txt"
        elif data[:4] == b"ff&A":
            suf = "ff"
        elif data[:1] == b";":
            suf = "txt"
        elif (data[:2] == b"\x06\x00" and data[2:4] != b"\x00\x00") or data[1:5] == b"\x00ec\x01":
            suf = "so"
        elif data[:3] == b"SCM":
            suf = "scm"
        elif data[:3] == b"EFM":
            suf = "efm"
        elif data[:8] == b"0\x00\x00\x00MOT\x00":
            suf = "mot2"
        elif data[:8] == b"`\x00\x00\x00CAM\x00":
            suf = "cam"
        elif data[:8] == b"0\x00\x00\x00HID\x00":
            suf = "hid3"
        elif data[:4] == b".TSC":
            suf = "tsc"
        elif b"# End" in data:
            suf = "txt"
        elif data[:4] == b"ipum":
            suf = "ipum"
        elif len(data) >= 3 and (
            (65 <= data[0] <= 90 and 65 <= data[1] <= 90 and 65 <= data[2] <= 90) or
            (97 <= data[0] <= 122 and 97 <= data[1] <= 122 and 97 <= data[2] <= 122)
        ):
            suf = data[:3].decode("ascii", errors="ignore")
        else:
            suf = "ukn"
    except Exception:
        suf = "ukn"
    return suf

def IPUM(data, ipum_name, pac_name):
    offs = 16
    num_files = unpack("<I", data[12:16])[0]
    try:
        os.mkdir(os.path.join(pac_name, ipum_name))
    except OSError:
        pass
    
    index_path = os.path.join(pac_name, ipum_name, f"{ipum_name}.index")
    with open(index_path, "w", encoding="utf-8") as index_file:
        for i in range(num_files):
            file_len = unpack("<I", data[offs+4:offs+8])[0]
            offs += 8
            file_data = data[offs:offs+file_len]
            offs += file_len
            index_file.write(f"{ipum_name}_{i:03d}.dds\n")
            try:
                file_path = os.path.join(pac_name, ipum_name, f"{ipum_name}_{i:03d}.dds")
                with open(file_path, "wb") as file_open:
                    file_open.write(file_data)
            except Exception:
                print(f"\tError Writing {ipum_name}_{i:03d}.dds")
    return 0

def PTX(data, ptx_name, pac_name):
    print(f"PTX Archive: {ptx_name}.ptx")
    num_files = unpack("<I", data[:4])[0]
    offsets = []
    last = 0
    tex_len = []
    
    for i in range(num_files):
        idx = data.find(b"DDS |", last)
        offsets.append(idx)
        last = idx + 4
        tex_len.append(unpack("<I", data[offsets[i]-12:offsets[i]-8])[0])
        
    try:
        os.mkdir(os.path.join(pac_name, ptx_name))
    except OSError:
        pass
        
    index_path = os.path.join(pac_name, ptx_name, f"{ptx_name}.index")
    with open(index_path, "w", encoding="utf-8") as index_file:
        for i in range(num_files):
            try:
                file_data = data[offsets[i]:offsets[i] + tex_len[i]]
            except IndexError:
                file_data = data[offsets[i]:]
            index_file.write(f"{ptx_name}_{i:03d}.dds\n")
            try:
                file_path = os.path.join(pac_name, ptx_name, f"{ptx_name}_{i:03d}.dds")
                with open(file_path, "wb") as file_open:
                    file_open.write(file_data)
            except Exception:
                print(f"\tError Writing {ptx_name}_{i:03d}.dds")
    return 0

def PTX2(data, ptx_name):
    print(f"PTX Archive: {ptx_name}.ptx")
    num_files = unpack("<I", data[:4])[0]
    offsets = []
    last = 0
    tex_len = []
    
    for i in range(num_files):
        idx = data.find(b"DDS", last)
        offsets.append(idx)
        last = idx + 4
        tex_len.append(unpack("<I", data[offsets[i]-12:offsets[i]-8])[0])
        
    try:
        os.mkdir(ptx_name)
    except OSError:
        pass
        
    index_path = os.path.join(ptx_name, f"{ptx_name}.index")
    with open(index_path, "w", encoding="utf-8") as index_file:
        for i in range(num_files):
            try:
                file_data = data[offsets[i]:offsets[i] + tex_len[i]]
            except IndexError:
                file_data = data[offsets[i]:]
            index_file.write(f"{ptx_name}_{i:03d}.dds\n")
            try:
                file_path = os.path.join(ptx_name, f"{ptx_name}_{i:03d}.dds")
                with open(file_path, "wb") as file_open:
                    file_open.write(file_data)
            except Exception:
                print(f"\tError Writing {ptx_name}_{i:03d}.dds")
    return 0

def walkdir(dirname):
    for root, dirs, files in os.walk(dirname):
        dirs.sort(key=natural_keys)
        files.sort(key=natural_keys)
        path = os.path.abspath(root)
        for filename in files:
            if filename.endswith(".pac"):
                Unpack(path, filename)

def Unpack(path, pac_file):
    pac_name = pac_file[:pac_file.find(".")]
    try:
        os.chdir(path)
    except Exception:
        print("nope")
        return -1

    print(f"Reading: {pac_file}")
    try:
        with open(pac_file, "rb") as pac_open:
            pac_data = pac_open.read()
    except Exception:
        print(f"Error Opening/Reading {pac_file}")
        return -1
    
    try:
        offsets = getFiles(pac_data)
        print(f"\nNumber of Files: {len(offsets)}\n")
    except Exception:
        print(f"Error Getting Contents of {pac_file}")
        return -1
    
    try:
        os.mkdir(pac_name)
    except OSError:
        pass
    
    index_path = os.path.join(pac_name, f"{pac_name}.index")
    with open(index_path, "w", encoding="utf-8") as index_file:
        if b"PNST" in pac_data[:4]:
            index_file.write("PNST\n")
            
        for i in range(len(offsets)):
            try:
                file_data = pac_data[offsets[i]:offsets[i+1]]
            except IndexError:
                file_data = pac_data[offsets[i]:]
            
            if b"ipum" in file_data[:5]:
                IPUM(file_data, f"{pac_name}_{i:03d}", pac_name)
                index_file.write(f"{pac_name}_{i:03d} vid\n")
            elif b"DDS |" in file_data[4:] and b"PAC." not in file_data[:5] and b"PNST" not in file_data[:5] and b"ipum" not in file_data[:5]:
                if b"DDS |" in file_data[112:117]:
                    index_file.write(f"{pac_name}_{i:03d}.dds\n")
                    try:
                        file_path = os.path.join(pac_name, f"{pac_name}_{i:03d}.dds")
                        with open(file_path, "wb") as file_open:
                            file_open.write(file_data[112:])
                    except Exception:
                        print(f"Error Writing {pac_name}_{i:03d}.dds")
                else:
                    PTX(file_data, f"{pac_name}_{i:03d}", pac_name)
                    index_file.write(f"{pac_name}_{i:03d} folder\n")
            else:
                ext = getType(file_data)
                index_file.write(f"{pac_name}_{i:03d}.{ext}\n")
                try:
                    file_path = os.path.join(pac_name, f"{pac_name}_{i:03d}.{ext}")
                    with open(file_path, "wb") as file_open:
                        file_open.write(file_data)
                except Exception:
                    print(f"Error Writing {pac_name}_{i:03d}.{ext}")

    global gotta_go_deep
    if gotta_go_deep:
        walkdir(pac_name)
    return 0

def main():
    global gotta_go_deep
    print("\n=================================\nDevil May Cry 3 \nPac extractor v1.8 (Python 3 Port)\n=================================\n")

    if len(sys.argv) < 2:
        gotta_go_deep = 1
        for root, dirs, files in os.walk("."):
            files.sort(key=natural_keys)
            path = os.path.abspath(root)
            for filename in files:
                if filename.endswith(".pac"):
                    Unpack(path, filename)

    elif len(sys.argv) == 3:
        gotta_go_deep = 1
        if sys.argv[2] == "all":
            pac_file = sys.argv[1]
            path = os.path.abspath(".")
            Unpack(path, pac_file)
        else:
            break_while = False
            break_loop = False
            for root, dirs, files in os.walk("."):
                dirs.sort(key=natural_keys)
                if break_loop:
                    break
                files.sort(key=natural_keys)
                path = os.path.abspath(".")
                for filename in files:
                    if filename != sys.argv[1] and not break_while:
                        continue
                    else:
                        break_while = True
                        if filename.endswith(".pac"):
                            Unpack(path, filename)
                    if filename == sys.argv[2]:
                        break_loop = True
                        break

    elif sys.argv[1].endswith(".ptx"):
        ptx_file = sys.argv[1]
        with open(ptx_file, "rb") as ptx_open:
            ptx_data = ptx_open.read()
        PTX2(ptx_data, ptx_file[:-4])
        
    elif sys.argv[1].endswith(".tm2"):
        with open(sys.argv[1], "rb") as read_str:
            file_data = read_str.read()
        with open(f"{sys.argv[1][:-3]}dds", "wb") as write_str:
            write_str.write(file_data[112:])
        
    else:
        pac_file = sys.argv[1]
        path = os.path.abspath(".")
        Unpack(path, pac_file)

    print(f"\nAll Done! {time.time() - time_start:.4f} sec")
    return 0

if __name__ == "__main__":
    main()