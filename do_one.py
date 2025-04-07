try:
    infile = snakemake.input[0]
except NameError:
    infile = "indata/Rog-Art-J-Gvecg-P500034.exb"

from lxml import etree
from pathlib import Path


def get_speaker_from_tiername(s: str) -> str:
    return s.split()[0]


doc = etree.fromstring(Path(infile).read_bytes())
tiers = doc.findall(".//tier")
speakers = list(
    set([get_speaker_from_tiername(i.attrib["display-name"]) for i in tiers])
)
timeline = {i.get("id"): float(i.get("time", 0)) for i in doc.findall(".//tli")}


def is_text_faulty(s: str | None) -> bool:
    if s is None:
        return True
    else:
        from re import match

        return not bool(match(r"PU\.tok\d+", s))


def fix_empty_PUs(PU_tier: etree._Element) -> None:
    for event in PU_tier.findall(".//event"):
        if is_text_faulty(event.text):
            # This means we have a weirdly named PU.
            start, end = event.get("start"), event.get("end")
            # print(
            #     f"Resolving PU with text: {event.text} file: {infile}, time: {timeline[start]}, "
            # )
            for tier in tiers:
                # Try and find traceability event:
                if not "traceability" in tier.get("display-name"):
                    continue
                hit = tier.find(f".//event[@start='{start}']")
                if hit is None:
                    continue
                else:
                    tok = hit.text.split(".tok")[1]
                    event.text = f"PU.tok{tok}"

                    # print("\tSetting reconciled PU text to", event.text)
                    # print("Fixed event attrib:", event.attrib)
                    break
            else:
                # This means that the PU does not lineup with other cells. Will skip this.
                event.text = f"PU.tokXXX"
                continue


def spot_fixes(e: etree._Element) -> None:
    if (e.text == "ok597") and (infile == "indata/Rog-Art-J-Gvecg-P500042.exb"):
        e.text = "PU.tok597"
    if (e.text == "ok1057") and (infile == "indata/Rog-Art-J-Gvecg-P500016.exb"):
        e.text = "PU.tok1057"
    if (e.get("start") == "Artur-J-Gvecg-P500034.t81_") and (
        e.get("end") == "Artur-J-Gvecg-P500034.t82_"
    ):
        e.text = "PU.tok650"
    if (e.get("start") == "Artur-J-Gvecg-P500034.t82_") and (
        e.get("end") == "Artur-J-Gvecg-P500034.t82.w0"
    ):
        e.getparent().remove(e)
    if (e.get("start") == "Artur-J-Gvecg-P500034.t108") and (
        e.get("end") == "Artur-J-Gvecg-P500034.t110"
    ):
        e.text = "PU.tok887"
    if (e.get("start") == "Artur-N-G5043-P600044.t33.w0") and (
        e.get("end") == "Artur-N-G5043-P600044.t34"
    ):
        e.text = "PU.tok147"
    if e.text == "PU.k1639PU.tok1640PU.tok1642":
        e.text = "PU.tok1640"
    if e.text == "PU.tok2030P":
        e.text = "PU.tok2030"
    if e.text == "PU.tok4528ok4506":
        e.text = "PU.tok4528"
    if e.text == "PU.tok1747P":
        e.text = "PU.tok1747"


for e in doc.findall(".//event"):
    spot_fixes(e)

for speaker in speakers:
    # Fix the naming of the PUs:
    t = doc.find(f".//tier[@display-name='{speaker} [prosodicUnits]']")
    assert t is not None, "No prosodic tier found!"
    fix_empty_PUs(t)

    # Spruce up possibly concatenated names (PU.tok1PU.tok2):
    for e in t.findall(".//event"):
        e.text = e.text.strip()
        text = e.text
        if text.count("PU") == 1:
            continue
        else:
            segs = text.split("PU")
            e.text = "PU" + segs[1]


# Validation:
for speaker in speakers:
    t = doc.find(f".//tier[@display-name='{speaker} [prosodicUnits]']")
    for event in t.findall(".//event"):
        from re import match

        p = r"^PU\.tok\d+$"
        if not bool(match(p, event.text)):
            print(
                f"PU to fix in : {infile}, {event.text=!r}, at {timeline[event.get('start')]}s, attrs: {event.attrib}"
            )

from datetime import date

today_formatted = date.today().strftime("%Y-%m-%d")
comment = doc.find(".//comment")
comment.text = (
    comment.text
    + f"  // {today_formatted}: Peter Rupnik: Rename and spruce up manually corrected prosodicUnits"
)
out_path = snakemake.output[0]

etree.indent(doc, space="\t")
doc.getroottree().write(
    Path(out_path),
    pretty_print=True,
    encoding="utf8",
    xml_declaration='<?xml version="1.0" encoding="UTF-8"?>',
)

Path(out_path).write_text(
    Path(out_path)
    .read_text()
    .replace(
        "<?xml version='1.0' encoding='UTF8'?>",
        '<?xml version="1.0" encoding="UTF-8"?>',
    )
)
