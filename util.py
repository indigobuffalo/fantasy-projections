import re


rows_total = '226 Adam Fantilli C CBJ 79 21 24 45 227 Andrew Copp LW/RW DET 79 13 33 46 228 Dustin Wolf G CGY 229 Bryan Rust LW/RW PIT 80 22 22 44 230 Alexis Lafrenière LW NYR 82 23 23 46 231 Jeremy Swayman G BOS 232 Ryan Hartman C MIN 80 20 25 45 233 Sam Bennett C/LW FLA 72 20 25 45 234 Nino Niederreiter LW/RW WPG 78 22 23 45 235 Christian Dvorak C/LW MTL 70 12 33 45 236 Kirill Marchenko LW/RW CBJ 80 23 22 45 237 Aaron Ekblad D FLA 54 6 22 28 238 Anthony Duclair LW/RW SJS 74 18 26 44 239 Victor Olofsson LW/RW BUF 81 22 22 44 240 Teuvo Teravainen LW/RW CAR 81 22 21 43 241 Marco Rossi C MIN 78 12 29 41 242 Jamie Drysdale D ANA 78 6 35 41 243 Gustav Nyquist LW/RW NSH 77 15 28 43 244 Brandon Saad LW/RW STL 78 21 22 43 245 Kaapo Kakko RW NYR 79 20 23 43 246 Peyton Krebs C/W BUF 76 15 28 43 247 J.J. Moser D ARI 80 9 33 42 248 Blake Coleman LW/RW CGY 81 18 25 43 249 Tommy Novak C NSH 82 16 27 43 250 Jack Roslovic C/RW CBJ 82 11 31 42'


def convert_to_int_safe(element):
    try:
        element = int(element)
    except ValueError:
        pass
    return element

def convert_to_csv(ep_line: list):
    first = ep_line.pop(1)
    last = ep_line.pop(1)
    ep_line.insert(1, f'{first} {last}')
    return ep_line

def split_ep_paste(blob: str):
    split = re.findall(r'(\d+ ([A-Za-z ])+ ([A-Z/])+([A-Z])* [A-Z]+ \d+ \d+ \d+ \d+)', blob)
    return [tup[0] for tup in split]


if __name__ == "__main__":
    csv_output = []
    res = split_ep_paste(rows_total)
    for x in res:
        csv_output.append(convert_to_csv(x.split(' ')))
    for p in csv_output:
        print(','.join(p))
