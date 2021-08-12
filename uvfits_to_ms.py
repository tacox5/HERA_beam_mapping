"""
Example:
casa -c uvfits_to_ms.py /path/to/data/*.uv
"""

from casa_imaging import convert_uvfits

if __name__ == "__main__":
    try:
        folders = sys.argv[3:]
        for folder in folders:
            convert_uvfits(folder)
    except IndexError:
        print("No file specified for conversion from uvfits to ms")
