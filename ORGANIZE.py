import os
import shutil
import time
import textwrap

def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))
def getnamefile(path):
    return os.path.basename(os.path.normpath(fixpath(path)))
 
color = {
    "yellow": "\033[93m",
    "red": "\033[91m",
    "green": "\033[32m",
    "default": "\033[0m"
}
indent = 5
os.system('cls' if os.name == 'nt' else 'clear')
print("\n\nLeave it blank if it's the current folder")
print('Folder path you want to sort files in',color["yellow"] + '(Drag folder here)', color["default"], end='')
target = input(': ')
print('Folder path where you want to save the sorted files ',color["yellow"] + '(Drag folder here)', color["default"], end='')
saveto = input(': ')
print('Include subfolder ?',color["yellow"] + '[y/n (default No)]', color["default"], end='')
subfolder = input(': ')
print('Overwrite File ?',color["yellow"] + '[y/n (default No)]', color["default"], end='')
overwrite = input(': ')

exclude_list = []
print("\n\nLeave it blank when finished or dont want to exclude")
print('Exclude folder you dont want to sort files in')
while True:
    print(color["yellow"] + '(Drag file/folder here)', color["default"], end='')
    exclude = input(': ')
    if not exclude:
        break
    else:
        exclude = exclude.replace('"', '')
        exclude_list.append(fixpath(exclude))

if not target or not saveto:
    if not target:
        target = fixpath('.\\')
    if not saveto:
        saveto = fixpath('.\\')
target = fixpath(target.replace('"',''))
saveto = fixpath(saveto.replace('"',''))
files = []
subfolder = True if subfolder.lower() == "y" else False
overwrite = True if overwrite.lower() == "y" else False

if subfolder:
    target = [x[0] for x in os.walk(target)]        #get all subdir in target path
    for list_subdir in target:
        check_files = os.listdir(list_subdir)       #get all files in all subdir
        for subdir_files in check_files:
            subdir_file_join = fixpath(os.path.join(list_subdir, subdir_files))
            files.append(subdir_file_join)          #append files list
else:
    for dir_files in os.listdir(target):
        dir_files_join = fixpath(os.path.join(target, dir_files))
        files.append(dir_files_join)
if overwrite:
    overwrite_status = "[Overwrite]"
else:
    overwrite_status = "[Skipping]"
    
#Exclude this script from being moved
if __file__ in files or __file__.replace('.py','.exe') in files:
    files.remove(fixpath(__file__))
    files.remove(fixpath(__file__.replace('.py','.exe')))   #exclude exe version



#Add extension by category in here, example YOUR_CATEGORY = {"extesion 1","extension 2"}
#underscore(_) mean space( )
#Extension by Category
Compressed = {"7z","arj","deb","pkg","rar","rpm","tar","gz","lzma","z","zip","dmg"}
Audio = {"aif","cda","mid","mp3","mpa","ogg","flac","wav","wma","m4a"}
Video = {"3gp","3gpp","avi","flv","m4v","mkv","mov","mp4","mpg","mpeg","rm","vob","wmv","ts","webm"}
Programs = {"exe","msi"}
Font = {"otf","ttf"}
Image = {"bmp","gif","ico","jpeg","jpg","png","tif","tiff","psd","heic","heif"}
Vector = {"ai","eps","cdr","svg","svgz"}
Documents = {"pps","pptx","ppt","xls","xlsm","xlsx","doc","docx","pdf","rtf","txt"}
Web = {"htm","html","webp","css","js"}
#Osu = {"osz","osr"}     #you can add (#) in front of the line to remove, or just delete the whole line
Flash = {"fla","swf"}
Android = {"apk"}
#EFI_file = {"efi"}
App = {"app"}
#add here, follow the example above

#Add your added category in here,
#if you remove them, then remove here too (recommended)
#Category List
category_list = {"Compressed",
                 "Audio",
                 "Video",
                 "Programs",
                 "Font","Image",
                 "Vector",
                 "Documents",
                 "Web",
                 "Osu",
                 "Flash",
                 "Android",
                 "EFI_file",
                 "App",
                 #add here, dont forget to add coma (,) in every line
                 }


file_list = []
os.system('color' if os.name == 'nt' else '')
print('')
#Exclude all category folder from checking subfolder (if the target folder are same)
for category in sorted(category_list):    
    print(color["yellow"] + '[Exclude]', color["default"] + 'category', color["green"] + category)
    print(color["default"], end='')
    to_remove = os.path.join(saveto, category)
    to_remove = to_remove.replace("_"," ")
    to_remove = [x for x in files if to_remove in x]
    for list in to_remove:
        files.remove(list)
    del to_remove
for exclude in sorted(exclude_list):
    print(color["yellow"] + '[Exclude]', color["green"] + list)
    print(color["default"], end='')
    to_remove = [x for x in files if exclude in x]
    for list in to_remove:
        files.remove(list)
    del to_remove
print('')
time.sleep(2)
for category in sorted(category_list):
    saveto_category = os.path.join(saveto, category)
    saveto_category = saveto_category.replace("_"," ")

    try:
        #Collecting list of file
        for ext in globals()[category]:
            for f in sorted(files):
                if f.lower().endswith('.{}'.format(ext)):
                    file_list.append(f)

        print('Checking files in category',color["yellow"] + '{}'.format(category))
        print(color["default"], end='')
        if file_list:
            print(' ' * indent, 'Moving files to', color["green"] + '{}'.format(saveto_category))
            print(color["default"], end='\n')
            while True:
                if os.path.exists(saveto_category):
                    for f in sorted(file_list):
                        if os.path.exists(fixpath(os.path.join(saveto_category, getnamefile(f)))):
                            print(' ' * indent, 'Already Exist', color["yellow"] + overwrite_status, end='')
                            print(color["default"], end=' ')
                            if subfolder:
                                print('{}'.format(f))
                            else:
                                print('{}'.format(getnamefile(f)))
                            if overwrite:
                                shutil.move(fixpath(f), os.path.join(fixpath(saveto_category), getnamefile(f)))
                            else:
                                pass
                            
                        else:
                            print(' ' * indent,color["yellow"] + '[Moving]', end='')
                            print(color["default"], end=' ')
                            
                            wrapper = textwrap.TextWrapper(width=50,
                                                           subsequent_indent=' '*15)
                            if subfolder:
                                print(wrapper.fill('{}'.format(f)))
                            else:
                                print(wrapper.fill('{}'.format(getnamefile(f))))
                            shutil.move(f, saveto_category)
                    file_list = []
                    break
                #Will create folder if not exist
                else:
                    print(color["yellow"] + ' ' * indent, '{}'.format(category), color["default"] + 'is Not Exist')
                    print(' ' * indent, 'Creating {}'.format(saveto_category))
                    print(' ' * indent,'---')
                    os.mkdir(saveto_category)

        else:
            print(' ' * indent,color["red"] + 'No files',color["default"] + 'in category',color["yellow"] + '{}'.format(category))
            print(color["default"], end='')
            print(' ' * indent,'---')
    except KeyError:
        pass
print("\n\nDone")
pause = input("Press Enter to continue...")

