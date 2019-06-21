import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

fid = "1SPq8YFb7LpjYVFcTiu8Q8AszWRXc_O-H"

loc = 'C:\\Users\\cmconnelly\\Desktop\\UploadData'

def file_upload(folder_id, src, setStatus):

    # folder_id: GoogleDriveFile['id']
    _q = {'q': "'{}' in parents and trashed=false".format(folder_id)}
    file_list = drive.ListFile(_q).GetList()
    fl = []
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        fl.append(file1['title'])

    num = 0
    src_files = os.listdir(src)
    os.chdir(src)
    for file_name in src_files:
        total = len(src_files)
        f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        if file_name not in fl:
            setStatus('Uploading {} of {}: {}'.format(num, total, file_name))
            num += 1
            f.SetContentFile(file_name)
            f.Upload()
        else:
            pass

        setStatus('finished uploading {} files'.format(num))


if __name__ == "__main__":
    main()
