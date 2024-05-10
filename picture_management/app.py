import json
import os
from PIL import Image
import pathlib

def getRatingFromImageXMP(file):
    if not os.path.exists(file): return 0

    with Image.open(file) as im:
        xmp = im.getxmp()

        # print(json.dumps(xmp, indent=3))

        if not xmp: return 0
        if not "xmpmeta" in xmp: return 0
        if not "RDF" in xmp["xmpmeta"]: return 0
        if not "Description" in xmp["xmpmeta"]["RDF"]: return 0
        if not "Rating" in xmp["xmpmeta"]["RDF"]["Description"]: return 0
        
        return  int(xmp["xmpmeta"]["RDF"]["Description"]["Rating"])
        
# path = "D:\\Data\\Pictures\\2022\\new\\2023\\2023-01\\2023-01-31\\"
# picFile = os.path.join(path, '20230131_131445.jpg')

# r = getRatingFromImageXMP(picFile)
# print(r)
# none = no raiting
# -1 = Reject
# 0,1,2,3,4,5

def add_new_afterall_year_monty_day_folders():
    path = "D:\\Data\\Pictures\\2022\\new\\2023"

    pl = pathlib.Path(path)

    g = pl.rglob("*")
    for e in g:
        if e.is_dir() and len(e.parents) == 7:        
            if "_new" not in (str(e)):
                print(len(e.parents), str(e)[len(path):])
                os.rename(str(e), str(e)+"_new")
# add_new_afterall_year_monty_day_folders()

def move_reject_pictures_to_reject_folder():
    # Zoek naar ge-"reject"-te fotos
    sourcepath = "D:\\Data\\Pictures\\2022"
    rejectpath = "D:\\Data\\Pictures\\2022 - Rejects"

    cnt = 0
    for e in pathlib.Path(sourcepath).rglob("*"):
        if not e.is_file(): continue
        if not e.suffix.lower() == ".jpg": continue
        rating = getRatingFromImageXMP(str(e))
        if rating != -1: continue

        cnt += 1
        sourceFile = str(e)
        sourcePath = str(e.parent)
        relSourcePath = sourcePath[len(sourcepath)+1:]    
        absRejectPath = os.path.join(rejectpath, relSourcePath)
        rejectFile = os.path.join(absRejectPath, e.name)
        print(cnt, 'source', sourceFile)
        #print('target path', absRejectPath)
        #print('target', rejectFile)

        if not os.path.exists(absRejectPath):
            os.makedirs(absRejectPath)

        os.rename(sourceFile, rejectFile)



        #if cnt == 100: break
    print('rejects:', cnt)
# move_reject_pictures_to_reject_folder()


def create_tree():
    sourcepath = "D:\\Data\\Pictures\\2022"

    tree = {}

    for e in pathlib.Path(sourcepath).rglob('*'):
        if not e.is_file(): continue
        suffix = e.suffix.lower()

        if not (suffix == ".mp4" or suffix == ".mov" or suffix == ".vsp" or suffix == ".kdenlive"): continue

        branch = tree
        for p in e.parts:
            if not p in branch: branch[p] = {}
            branch = branch[p]


        # if not suffix in s: s[suffix] = { "cnt": 0, "size": 0 }
        # s[suffix]["cnt"] += 1
        branch["size"] = e.stat().st_size
        branch["isFile"] = True


    # print(json.dumps(tree, indent=3))
    with open('tree.json', 'w') as f:
        f.write(json.dumps(tree, indent=3))
# create_tree()

def humanbytes(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)



def travel(parentNode, level = 0):
    
    totalSize = 0
    #, path=[], level=0, sizetree: dict = { "size": 0, "count": 0, "items": {} }
    treeSize = {}

    for name, node in parentNode.items():
    #     name = name.replace('\\', '')

        if not "isFile" in node:
            (size, node) = travel(node, level + 1)
            treeSize[name] = node
            totalSize+=size

            pass
    #         # if not name in sizePerLevel: sizePerLevel[name] = { "size": 0, "count": 0 }
    #         # print('dir', level, name)
    #         if not name in sizetree:
    #             sizetree[name] = { "size": 0, "count": 0, "items": {} }

    #         totalSize += travel(node, path + [name], level+1, sizetree[name])
        else:
            pass
    #         size = node["size"]
    #         totalSize+=size

    #         # node = sizePerLevel
    #         # for item in path:
    #         #     print(item, sizePerLevel)
    #         #     current = node[item]
    #         #     current["size"] += size
    #         #     node = current
    
    #         #print('file', level, name, size, humanbytes(size), '\\'.join(path))
        
    
    return (totalSize, treeSize)

def x():
    with open('tree.json', 'r') as f:
        tree = json.load(f)
        
    #totalSize, sizetree = 
    travel(tree)
    #print(humanbytes(totalSize))
    #print(json.dumps(sizetree, indent=3))
    # 2.34 TB
    #sorted()

x()


# TODO:
# > update picture frame...wordt Arik nog steeds uit gefiltered. dat hoeft dus niet meer.
# > ook label's zetten op dagen
# > wellicht ook arik in correct folder zetten. er zijn feel mappen met alleen plaatjes van arik die niet in Arik map zitten.
# > movie pictures and video's from almost empty folders to month...note..there could be many vidoe's these we did not sort yet
#    dit wil ik niet van elke folder doen, dus dit in kaart brengen en dan zelf met de hand d ekeuze maken ja of nee naar maand fodler root.
#    check % van folders gevuld met foto's. als dit lager is dan x dan rapporteren. Deze foto's dan verplaatsen naar maand.?

# remove empty folders. .. empty folders kunnen gelaagd zijn..2022-05-28/movie     empty
                                                           #  2022-05-28/private   empty
                                                           #  2022-05-28/          empty als mappen weg zijn.

# 5) cleanup video's.
                # doe ook een movie van arik videos naar de arik folder.
# 6) remove large videos.

# exclud from picture frame: 2022-00-Fotoboek-Arik-(alma en ik later afrmaken)


# Finish this one later with alma:
# D:\Data\Pictures\2022\2022-00-Fotoboek-Arik-(alma en ik later afrmaken)\
