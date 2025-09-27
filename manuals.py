#!/usr/bin/env python
import os
import subprocess
import time
from PyPDF2 import PdfReader
import psutil

# Path to SumatraPDF executable
SUMATRA_PATH = r"C:\portableapps\sumatrapdf\sumatrapdf.exe"

# Folders where PDFs are stored
PDF_FOLDERS = [
    r"C:\Users\benoi\Downloads\ebay_manuals",
    r"C:\Users\benoi\Downloads\manuals"
]

# Available printers
PRINTERS = {
    "1": "Brother HL-L8360CDW [Wireless]",
    "2": "Brother HL-L8360CDW series"
}

# Predefined print settings for specific PDFs (keys stored in lowercase)
PRINT_SETTINGS = {
    "singer 3337": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,duplex,fit,paper=letter",
        "monochrome,3-34,duplex,fit,paper=letter",
        "color,102,simplex,fit,paper=letter",
    ],
    "singer 5500": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,duplex,fit,paper=letter",
        "monochrome,3-64,duplex,fit,paper=letter",
    ],
    "ti-81": [
        "monochrome,1-193,duplex,fit,paper=letter",
    ],
    "tandy 100": [
        "monochrome,1-230,duplex,fit,paper=letter",
    ],
    "hp87": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-64,duplex,fit,paper=letter",
    ],
    "singer 4432": [
        "color,1,simplex,fit,paper=letter,landscape",
        "monochrome,2,duplexshort,fit,paper=letter,landscape",
        "monochrome,3-35,duplexshort,fit,paper=letter,landscape",
    ],
    "kodak pixpro az528": [
        "color,1,simplex,fit,paper=letter,landscape",
        "monochrome,3-124,duplexshort,fit,paper=letter,landscape",
    ],
    "hp27s19b-tech-en": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-110,duplex,fit,paper=letter",
    ],
    "hp35-survey-en": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-66,duplex,fit,paper=letter",
    ],
    "hp35s-surveying-solutions": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-72,duplex,fit,paper=letter",
    ],
    "akai m-9": [
        "color,1,simplex,fit,paper=letter,landscape",
        "monochrome,2,duplexshort,fit,paper=letter,landscape",
        "monochrome,3-26,duplexshort,fit,paper=letter,landscape",
    ],
    "otari mtr-10ii": [
        "monochrome,1-180,duplex,fit,paper=letter",
        "color,181,188,duplex,fit,paper=letter",
        "monochrome,189-290,duplex,fit,paper=letter",
    ],
    "hp41c41cv41cx-sm-en": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-210,duplex,fit,paper=letter",
    ],
    "red epic scarlet": [
        "color,1-248,duplex,fit,paper=letter",
    ],
    "blackmagic cinema camera and production camera": [
        "color,1-43,duplexshort,fit,paper=letter,landscape",
    ],
    "red dsmc2 dragon-x": [
        "color,1-236,duplex,fit,paper=letter",
    ],
    "baby lock ble1at-2-instruction-manual": [
        "color,1-54,duplex,fit,paper=letter",
    ],
    "tektronix mso22": [
        "color,1-257,duplex,fit,paper=letter",
    ],
    "hp15c-oh-en": [
        "color,1-300,duplex,fit,paper=letter",
    ],
    "singer 2263": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,duplex,fit,paper=letter",
        "monochrome,3-62,duplex,fit,paper=letter",
    ],
    "bernette b05": [
        "color,1-82,duplex,fit,paper=letter",
    ],
    "tandy 100 service manual": [
        "monochrome,1-127,duplex,fit,paper=letter",
    ],
    "nikon z6 z7 user": [
        "monochrome,1-272,duplex,fit,paper=letter",
    ],
    "zoom hd8": [
        "monochrome,1-213,duplex,fit,paper=letter",
    ],
    "nikon d7200": [
        "monochrome,1-416,duplex,fit,paper=letter",
    ],
    "nikon d4": [
        "monochrome,1-484,duplex,fit,paper=letter",
    ],
    "sony pxw-fs7": [
        "monochrome,1-145,duplex,fit,paper=letter",
    ],
    "hp97-sm-en": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-159,duplex,fit,paper=letter",
        "color,160,simplex,fit,paper=letter",
    ],
    "hp71-sm-en": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-158,duplex,fit,paper=letter",
    ],
    "hp75-sm-en": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-137,duplex,fit,paper=letter",
        "color,138,simplex,fit,paper=letter",
    ],
    "canon powershot sx40hs": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,simplex,fit,paper=letter",
        "monochrome,3-219,duplex,fit,paper=letter",
    ],
    "bernette b77": [
        "color,1-103,duplex,fit,paper=letter",
    ],
    "pioneer dvl-909": [
        "monochrome,1,simplex,fit,paper=letter",
        "monochrome,3,simplex,fit,paper=letter",
        "monochrome,140,duplex,fit,paper=letter",
    ],
    "boss br-1200cd": [
        "monochrome,1-364,duplex,fit,paper=letter",
    ],
    "tektronix 475": [
        "monochrome,1-240,duplex,fit,paper=letter",
    ],
    "panasonic gh2": [
        "monochrome,1-208,duplex,fit,paper=letter",
    ],
    "olympus om-1": [
        "monochrome,1-342,duplex,fit,paper=letter",
    ],
    "yaesu ft-991 transceiver": [
        "monochrome,1-158,duplex,fit,paper=letter",
    ],
    "nikon d800": [
        "monochrome,1-472,duplex,fit,paper=letter",
    ],
    "pentax 645z": [
        "color,1,simplex,fit,paper=letter",
        "color,2,simplex,fit,paper=letter",
        "color,3-112,duplexshort,fit,paper=letter",
    ],
    "pentax 645d": [
        "color,1,simplex,fit,paper=letter",
        "color,2,simplex,fit,paper=letter",
        "color,3-108,duplexshort,fit,paper=letter",
    ],
    "canon powershot sx530 hs": [
        "color,1-169,duplexshort,fit,paper=letter,landscape",
    ],
    "pentax k3 iii": [
        "monochrome,1,simplexshort,fit,paper=letter,landscape",
        "monochrome,2,simplexshort,fit,paper=letter,landscape",
        "monochrome,3-148,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx700 hs": [
        "color,1-198,duplexshort,fit,paper=letter,landscape",
    ],
    "kodak pixpro az252": [
        "color,1-96,duplexshort,fit,paper=letter,landscape",
    ],
    "minolta mn67z": [
        "color,1-139,duplexshort,fit,paper=letter,landscape",
    ],
    "leica sl2": [
        "color,1-220,duplexshort,fit,paper=letter,landscape",
    ],
    "leica sl2-s": [
        "color,1-299,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx710 hs": [
        "color,1-177,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx430 is": [
        "color,1-146,duplexshort,fit,paper=letter,landscape",
    ],
    "leica sl": [
        "color,1-146,duplexshort,fit,paper=letter,landscape",
    ],
    "hp48g-qsg-en": [
        "color,1-116,duplex,fit,paper=letter,landscape",
    ],
    "hp48g-qsg-en": [
        "color,1-116,duplex,fit,paper=letter,landscape",
    ],
    "canon powershot sx540 hs": [
        "color,1-186,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx740 hs": [
        "color,1-130,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx530 hs": [
        "color,1-169,duplexshort,fit,paper=letter,landscape",
    ],
    "voicelive 3": [
        "color,1-186,duplexshort,fit,paper=letter,landscape",
    ],
    "voicelive 3 extreme": [
        "color,1-202,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx720 hs": [
        "color,1-185,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx610 hs": [
        "color,1-162,duplexshort,fit,paper=letter,landscape",
    ],
    "leica q3": [
        "color,1-269,duplexshort,fit,paper=letter,landscape",
    ],
    "minolta mn40z": [
        "color,1-105,duplexshort,fit,paper=letter,landscape",
    ],
    "leica q2": [
        "color,1-233,duplexshort,fit,paper=letter,landscape",
    ],
    "brother innov-is xp3 embroidery": [
        "color,1-212,duplex,fit,paper=letter",
    ],
    "brother xr1355": [
        "color,1-112,duplex,fit,paper=letter",
    ],
    "humminbird helix 5": [
        "color,1-215,duplex,fit,paper=letter",
    ],
    "ricoh grii": [
        "color,1-184,duplex,fit,paper=letter",
    ],
    "ricoh griii": [
        "color,1-170,duplex,fit,paper=letter",
    ],
    "panasonic dmc-fz1000": [
        "color,1-367,duplex,fit,paper=letter",
    ],
    "humminbird helix series operations manual": [
        "color,1-348,duplex,fit,paper=letter",
    ],
    "canon xa70 xa75": [
        "color,1-154,duplex,fit,paper=letter",
    ],
    "leica q3 43": [
        "color,1-264,duplex,fit,paper=letter",
    ],
    "leica d-lux 7": [
        "monochrome,2,simplex,fit,paper=letter",
        "color,3-293,duplex,fit,paper=letter",
    ],
    "leica d-lux 8": [
        "color,1-215,duplex,fit,paper=letter",
    ],
    "canon eos 5d mark iv": [
        "color,1-676,duplex,fit,paper=letter",
    ],
    "lowrance hds pro": [
        "color,1-288,duplex,fit,paper=letter",
    ],
    "canon eos m50 mark ii": [
        "color,1-709,duplex,fit,paper=letter",
    ],
    "nikon df": [
        "monochrome,1-396,duplex,fit,paper=letter",
    ],
    "yamaha dgx-670": [
        "monochrome,1-116,duplex,fit,paper=letter",
    ],
    "yamaha dgx-670 - reference": [
        "color,1-93,duplex,fit,paper=letter",
    ],
    "nikon d3100 reference": [
        "monochrome,1-214,duplex,fit,paper=letter",
    ],
    "jvc gy-hm200u": [
        "monochrome,1-184,duplex,fit,paper=letter",
    ],
    "red dsmc2 helium": [
        "color,1-238,duplex,fit,paper=letter",
    ],
    "bernina 570qe": [
        "color,1-214,duplex,fit,paper=letter",
    ],
    "husqvarna viking designer i": [
        "color,1-117,duplex,fit,paper=letter",
    ],
    "husqvarna viking emerald": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-46,duplex,fit,paper=letter",
        "color,47-48,duplex,fit,paper=letter",
    ],
    "yamaha dgx-230": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-120,duplex,fit,paper=letter",
    ],
    "bernina virtuosa 153 163": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,simplex,fit,paper=letter",
        "monochrome,3-71,duplex,fit,paper=letter",
    ],
    "hp16c-oh-en": [
        "color,1-140,duplex,fit,paper=letter",
    ],
    "hp42s-elec-en": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-164,duplex,fit,paper=letter",
    ],
    "olympus tg-6": [
        "monochrome,1-166,duplex,fit,paper=letter",
    ],
    "olympus e-m5": [
        "monochrome,1-133,duplex,fit,paper=letter",
    ],
    "olympus e-510": [
        "monochrome,1-140,duplex,fit,paper=letter",
    ],
    "olympus tg-5": [
        "monochrome,1-134,duplex,fit,paper=letter",
    ],
    "hp42s-elec-en": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-164,duplex,fit,paper=letter",
    ],
    "gopro hero 9 black camera": [
        "color,3-145,duplex,fit,paper=letter",
    ],
    "baby lock blsa3-embroidery": [
        "color,3-191,duplex,fit,paper=letter",
    ],
    "baby lock blsa3-sewing": [
        "color,3-215,duplex,fit,paper=letter",
    ],
    "baby lock blsa3-embroidery-design-guide": [
        "color,3-191,duplex,fit,paper=letter",
    ],
    "hp42s-easycourse": [
        "monochrome,3-388,duplex,fit,paper=letter",
    ],
   "hp15c-ce-afh-en": [
        "color,1-227,duplex,fit,paper=letter",
    ],
    "hp15c-ce-oh-en": [
        "color,1-307,duplex,fit,paper=letter",
    ],
    "hp15c-oh-en": [
        "color,1-300,duplex,fit,paper=letter",
    ],
    "hp15c-afh-en": [
        "color,1-228,duplex,fit,paper=letter",
    ],
    "ti nspire cxii cas guidebook": [
        "color,1-97,duplex,fit,paper=letter",
    ],
    "pfaff creative icon": [
        "color,1-211,duplex,fit,paper=letter",
    ],
    "ti nspire cx reference": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-70,duplex,fit,paper=letter",
        "monochrome,71-150,duplex,fit,paper=letter",
        "monochrome,71-150,duplex,fit,paper=letter",
        "monochrome,151-204,duplex,fit,paper=letter",
        "color,205-226,duplex,fit,paper=letter",
        "monochrome,227-254,duplex,fit,paper=letter",
    ],
    "hp12c-oh-en": [
        "color,1-252,duplex,fit,paper=letter",
    ],
    "hp42s-easycourse": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,3-100,duplex,fit,paper=letter",
        "monochrome,101-200,duplex,fit,paper=letter",
        "monochrome,201-300,duplex,fit,paper=letter",
        "monochrome,301-388,duplex,fit,paper=letter",
    ],
    "hp12c-ce-oh-en": [
        "color,1-252,duplex,fit,paper=letter",
    ],
    "panasonic gx1": [
        "color,1-225,duplex,fit,paper=letter",
    ],
    "nikon coolpix p950": [
        "color,1-308,duplex,fit,paper=letter",
    ],
    "tascam dp-03sd": [
        "monochrome,1-76,duplex,fit,paper=letter",
    ],
    "tascam dp-24sd": [
        "color,1-80,duplex,fit,paper=letter",
    ],
    "boss dr-880": [
        "monochrome,1-168,duplex,fit,paper=letter",
    ],
    "boss dr-880": [
        "monochrome,1-168,duplex,fit,paper=letter",
    ],
    "brother jx2517": [
        "monochrome,1-40,duplex,fit,paper=letter",
    ],
    "sony f65": [
        "monochrome,1-98,duplex,fit,paper=letter",
    ],
    "kodak pixpro fz55": [
        "color,1-83,duplexshort,fit,paper=letter,landscape",
    ],
    "lowrance hook series": [
        "color,1-57,duplexshort,fit,paper=letter,landscape",
    ],
    "akai 4000ds mk2": [
        "color,1-18,duplexshort,fit,paper=letter,landscape",
    ],
    "canon powershot sx420 is": [
        "color,1-149,duplexshort,fit,paper=letter,landscape",
    ],
    "hp82441a-om-en": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-156,duplex,fit,paper=letter",
    ],
    "hp82441a-om-en": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-156,duplex,fit,paper=letter",
    ],
    "hp82104a-sm-en": [
        "color,1-2,duplex,fit,paper=letter",
        "monochrome,3-38,duplex,fit,paper=letter",
    ],
    "hp82211a-om-en": [
        #"color,1,simplex,fit,paper=letter",
        "monochrome,2,simplex,fit,paper=letter",
        "monochrome,3-100,duplex,fit,paper=letter",
        "monochrome,101-200,duplex,fit,paper=letter",
        "monochrome,201-240,duplex,fit,paper=letter",
    ],
    "nikon d3500": [
        "monochrome,1-36,duplex,fit,paper=letter",
    ],
    "nikon d3300": [
        "monochrome,1-144,duplex,fit,paper=letter",
    ],
    "nikon d6 reference": [
        "color,1-1202,duplex,fit,paper=letter",
    ],
    "nikon d5": [
        "monochrome,1-420,duplex,fit,paper=letter",
    ],
    "panasonic g7": [
        "color,1-76,duplex,fit,paper=letter",
    ],
    "sony pmw-f55": [
        "monochrome,1-150,duplex,fit,paper=letter",
    ],
    "jvc gy-hm250u gy-hm250e_v2": [
        "monochrome,1-212,duplex,fit,paper=letter",
    ],
    "jvc gy-hm250u gy-hm250e": [
        "monochrome,1-200,duplex,fit,paper=letter",
    ],
    "nikon d850": [
        "monochrome,1-400,duplex,fit,paper=letter",
    ],
    "wp34s-bg-en": [
        "color,1-187,duplex,fit,paper=letter",
    ],
    "brother innov-is xp2 embroidery design guide": [
        "color,1-40,duplex,fit,paper=letter",
        "color,41-80,duplex,fit,paper=letter",
        "color,81-120,duplex,fit,paper=letter",
        "color,121-156,duplex,fit,paper=letter",
    ],
    "brother innov-is xp2 embroidery": [
        "color,1-216,duplex,fit,paper=letter",
    ],
    "brother innov-is xp2 sewing": [
        "color,1-236,duplex,fit,paper=letter",
    ],
    "nikon d6": [
        "monochrome,1-316,duplex,fit,paper=letter",
    ],
    "nikon d780": [
        "monochrome,1-132,duplex,fit,paper=letter",
    ],
    "hp71-rpn": [
        "monochrome,1-12,duplex,fit,paper=letter",
    ],
    "tascam dp-02": [
        "monochrome,1-80,duplex,fit,paper=letter",
    ],
    "canon eos 6d": [
        "color,1-404,duplex,fit,paper=letter",
    ],
    "hp6797-pac-eleceng-en": [
        "color,1-138,duplex,fit,paper=letter",
    ],
    "dm42": [
        "color,1-29,duplex,fit,paper=letter",
    ],
    "brother sq-9185": [
        "color,1-116,duplex,fit,paper=letter",
    ],
    "dm41x_user_manual": [
        "color,3-44,duplex,fit,paper=letter",
    ],
    "tandy 100 hidden power": [
        "monochrome,2,simplex,fit,paper=letter",
        "monochrome,3-257,duplex,fit,paper=letter",
    ],
    "canon powershot sx30 is": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,simplex,fit,paper=letter",
        "monochrome,3-196,duplex,fit,paper=letter",
    ],
    "tandy 100 reference": [
        "color,1,simplex,fit,paper=letter",
        "monochrome,2,simplex,fit,paper=letter",
        "monochrome,3-126,duplex,fit,paper=letter",
    ],
    "brother ce8080 ce8080prw": [
        "color,1-72,duplex,fit,paper=letter",
    ],
}

def other_python_scripts_running():
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == 'python.exe' and proc.info['pid'] != current_pid:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def select_printer():
    """Prompts the user to select a printer."""
    print("\nSelect a printer:")
    for key, name in PRINTERS.items():
        print(f"{key}. {name}")
    
    choice = input("Enter the number of the printer: ").strip()
    return PRINTERS.get(choice, PRINTERS["1"])

def find_pdf(partial_name):
    """Finds a PDF file in the specified folders that contains the given string (case insensitive)."""
    partial_name_lower = partial_name.lower()

    matching_files = []
    for folder in PDF_FOLDERS:
        for f in os.listdir(folder):
            if f.lower().endswith(".pdf") and partial_name_lower in f.lower():
                matching_files.append(os.path.join(folder, f))

    if not matching_files:
        print(f"No PDF found containing: {partial_name}")
        return None
    
    if len(matching_files) > 1:
        print("\nMultiple matches found:")
        for idx, file in enumerate(matching_files, start=1):
            print(f"{idx}. {os.path.basename(file)}")
        choice = input("\nEnter the number of the file you want to print: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(matching_files):
            print("Invalid choice.")
            return None
        return matching_files[int(choice) - 1]

    return matching_files[0]  # Return the only match

def get_pdf_page_count(pdf_path):
    """Returns the number of pages in the given PDF file."""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            return len(reader.pages)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def print_pdf(printer_name, partial_name):
    """Prints a PDF with predefined settings or user-defined page ranges."""
    pdf_path = find_pdf(partial_name)
    if not pdf_path:
        return

    # Display the number of pages in the selected PDF
    page_count = get_pdf_page_count(pdf_path)
    if page_count:
        print(f"The document '{os.path.basename(pdf_path)}' has {page_count} pages.")
    else:
        print("Unable to determine the number of pages.")

    file_name_without_ext = os.path.splitext(os.path.basename(pdf_path))[0].lower()
    
    # Get predefined print settings 
    print_settings = PRINT_SETTINGS.get(file_name_without_ext, [f"color,1-{page_count},fit,paper=letter"])
    print("")
    print(f"Found settings for {pdf_path}:")
    for setting in print_settings:
        print(setting)
        if "landscape" in setting:
            printer_name1 = printer_name.replace("Wireless","Landscape")
        else:
            printer_name1 = printer_name

    # Get custom page range input
    custom_range = input("\nEnter the page range to print (e.g., 40-215), or press Enter for default: ").strip()

    # print("Wait for other jobs to finish...")
    
    # while other_python_scripts_running():
    #     time.sleep(10)

    # print("All other jobs are done. Proceeding...")

    anew = 0
    
    if custom_range:
        print_settings_copy = print_settings
        new_print_settings = []
        for setting in print_settings:
            setting_parts = setting.split(",")
            modified_setting = []
            
            for part in setting_parts:
                if "-" in part and part.replace("-", "").isdigit():
                    if anew ==0: 
                        a = int(part.split('-')[0])
                    else:
                        a = anew
                    b = int(part.split('-')[1])
                    a1 = int(custom_range.split('-')[0])
                    b1 = int(custom_range.split('-')[1])
                    if a1>b or b1<a:
                        pass
                    else:
                        a2 = max(a1,a)
                        b2 = min(b1,b)
                        anew  = b+1
                        modified_setting.append(f"{a2}-{b2}")
                        new_print_settings.append(",".join(modified_setting))
        parts = print_settings[0].split(',')
        parts[1] = f"{a2}-{b2}"
        print_settings = [','.join(parts)]
        new_page_count = min(page_count,b2)
    else:
        new_page_count = page_count

    print(f"Printing: {os.path.basename(pdf_path)} on {printer_name1}...")

    batch_size = 70  # Number of pages per batch
    delay_between_batches = 240  # Delay in seconds between batches
    if printer_name == "Brother HL-L3290CDW [Wireless]":
        delay_between_batches = 480  # Delay in seconds between batches

    for setting in print_settings:
        # Extract page range from the setting
        setting_parts = setting.split(",")
        page_range = None
        for part in setting_parts:
            if ("-" in part and part.replace("-", "").isdigit()):
                page_range = part
                break
            elif (part.isdigit()):
                #print a single page
                print(f"Printing page {part}")
                subprocess.run([SUMATRA_PATH, "-print-to", printer_name1, "-print-settings", setting, pdf_path], check=True)
                time.sleep(10)
        if page_range:
            start_page, end_page = map(int, page_range.split("-"))
            current_page = start_page

            while current_page <= end_page:
                batch_end = min(current_page + batch_size - 1, end_page)
                batch_range = f"{current_page}-{batch_end}"
                batch_setting = setting.replace(page_range, batch_range)

                print(f"Printing pages {batch_range}")
                subprocess.run([SUMATRA_PATH, "-print-to", printer_name1, "-print-settings", batch_setting, pdf_path], check=True)

                current_page += batch_size
                if current_page <= new_page_count:
                    print(f"Waiting for {delay_between_batches // 60} minutes before next batch...")
                    time.sleep(delay_between_batches)

if __name__ == "__main__":
    selected_printer = select_printer()
    file_name = input("\nEnter part of the PDF filename: ").strip()

    print_pdf(selected_printer, file_name)

 

