# firmware-lge-joan-blobs

Proprietary firmware for the LG V30 (joan), hosted so postmarketOS packaging can
fetch it by commit-pinned URL — the way `TheMuppets`, `FairBlobs` and
`sm6115-mainline` host blobs for other devices. The packaging lives in
[`lg-v30-joan-pmos-packages`](https://github.com/ShapeShifter499/lg-v30-joan-pmos-packages)
and stays text-only.

## Layout

| tree | contents |
|---|---|
| `common/` | A540 GPMU and QCA Bluetooth firmware — identical on every joan |
| `h930/` | modem, ADSP, SLPI (sensor DSP), Venus (video codec), IPA, WLAN and zap shader for **H930, US998, H932PR and every other joan** |
| `h932/` | the same set for an **exact LG-H932** |

`MANIFEST.tsv` lists every file as `tree`, install path, size and **sha256**.

## Why two variant trees

The H932 is the T-Mobile model and is signed with different keys. Measured
against stock firmware of the same Android release (`US99830b` and `H93230d`,
both Pie, both reporting Qualcomm build `MPSS.AT.2.5.c1.2-00056`), **38 of 47
files differ**. Same build, different signatures. The nine that happen to match
are individual segments and are not usable on their own: an image's `.mdt`
signs the segment hash table, so a set has to come from one device.

This is the same split LineageOS makes when it detects an H932 at flash time.
With a package manager the choice can simply be a package instead.

The zap shader is the only firmware where a cross-family payload is known to
work: the `h930` zap runs on a US998, verified on hardware.

## Provenance

`h930/` comes from a US998 on Pie `30b`; `h932/` from the `H93230d` KDZ.
The Venus and SLPI images come from the same sources: the `h930` set from that
US998's NON-HLOS (`modem`) partition, whose `modem.mdt` and `adsp.mdt` match
the `h930` rows above byte for byte, and the `h932` set from the KDZ's
`modem` image (KDZ md5 `eea31e240d28ee36efb3b3ee9a7533ec`). Neither set is
shared: Venus differs in 2 of 6 files (the signed `.mdt` among them) and
SLPI v2 in 13 of 15, so each variant carries its own. Only `slpi_v2` ships;
`slpi_v1` is for pre-production v1 silicon.
`common/` is mirrored from commit-pinned TheMuppets vendor trees.

WLAN `board.bin` is the **stock generic** board data from each variant's system
image, not per-unit factory calibration from any particular handset.

## Licence

`LICENSE.qcom` and `NOTICE.txt` are the Qualcomm licence and third-party
attribution notice as carried by `linux-firmware`. The licence permits binary
redistribution on condition that the terms file ships with it and notices are
not removed, which is why both are here.

The zap shader is signed by LG rather than Qualcomm, and these images came off
retail devices rather than from QTI. No ownership is claimed and no licence
beyond the above is granted or implied. If you hold rights to any file here and
want it removed, open an issue and say which files, so the rest can keep
working.
