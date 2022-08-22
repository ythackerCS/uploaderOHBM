import os
import sys
import requests
from pyxnat import Interface

# General arguments


# xnat_URL_users = "https://demo.xnat.org/xapi/users"
# users_to_exclude = ["admin", "guest", "kelseym", "stlstevemoore", "ythacker", "satrajit", "emma", "emma_test",
#                     "adameggebrecht", "kelseym_owner", "ari"]


project_id = "NEURODOT_FNIRS_DEMO_"
login = "username"
pas = "password"
xnat_url = "https://demo.xnat.org"
xnat_url_users = xnat_url + "/xapi/users"
users_to_exclude = ["admin", "guest", "kelseym", "stlstevemoore","satrajit", "emma", "emma_test", "adameggebrecht", "kelseym_owner", "ari", "smoore", "ythacker", 'emma2', 'arisegel_is_cool']

new_users_projects_created = []


data_file_path = "./Data/"
a_mat_file_path = "./A_matricies"
e_mat_file_path = "./E_matricies"
mni_mat_file_path = "./MNI_files"
params_file_path = "params.txt"
params_file_path2 = "params2.txt"

# verify and enable users:
with requests.session() as s:
    # set credentials
    s.auth = (login, pas)

    # establish interface with xnat
    interface = Interface(server=xnat_url, user=login, password=pas)

    # get the list of users
    r = s.get(xnat_url_users)

    # everything failed, all is lost
    if r.status_code > 201:
        # farewell cruel world
        raise RuntimeError("Got status {status}: {message}".format(status=r.status_code, message=r.text))

    # get user list as json
    users = r.json()

    for user in users:
        userinfo = xnat_url+"/xapi/users/{username}".format(username = user)
        r = s.get(userinfo)
        info = r.json()
        verfied =  info["verified"]
        enabled = info["enabled"]

        if not verfied: 
            payload = {"verified": "true"}
        if not enabled: 
            payload = {"enabled": "true"}
        if not verfied and not enabled: 
            payload = {"enabled": "true", "verified": "true"}

        if user not in users_to_exclude:
            # enabling and verifying user
            if not verfied or not enabled:
                print("Enabling user ", user)
                r = s.put(xnat_url_users + "/" + user, json=payload)
                if r.status_code > 201:
                    print("Error updating user {user}: [{status}] {message}".format(user=user, status=r.status_code,
                                                                                    message=r.text), file=sys.stderr)
                    # don't attempt the other stuff since something's wrong with this user
                    continue

            

            project_name = project_id + user
            my_project = interface.select.project(project_name)

            # #creating subjects loop
            if not my_project.exists() or len(my_project.subjects().get()) < 11:
                print("Project did not exist/ was incomplete, creating project ", project_name)
                my_project.create()

                # adding user to project
                member_url = xnat_url + "/data/projects/{project}/users/{project}_owner/{username}".format(project=project_name, username=user)
                r = s.put(member_url)
                print("Added ", user, " to project ", project_name, "\n", r)


                #project level files to upload 
                print("Uploading project level files: ")

                #A_MAT UPLOADING
                print("Uploading A_MAT folder ")
                resouce = my_project.resource("A_matricies")
                if not resource.exists():
                        resource.create()
                file_list = [name for name in os.listdir(a_mat_file_path)]
                for file in file_list:
                    #upload resource file
                    local_resource = (os.path.join(a_mat_file_path, file))
                    fileName = file

                    # print("Uploading subject resource... ", local_resource)
                    resource.file(fileName).insert(local_resource)


                #E_MAT UPLOADING
                print("Uploading E_MAT folder ")
                resouce = my_project.resource("E_matricies")
                if not resource.exists():
                        resource.create()
                file_list = [name for name in os.listdir(e_mat_file_path)]
                for file in file_list:
                    #upload resource file
                    local_resource = (os.path.join(e_mat_file_path, file))
                    fileName = file

                    # print("Uploading subject resource... ", local_resource)
                    resource.file(fileName).insert(local_resource)


                #mni_MAT UPLOADING
                print("Uploading MNI_MAT folder ")
                resouce = my_project.resource("MNI_files")
                if not resource.exists():
                        resource.create()
                file_list = [name for name in os.listdir(mni_mat_file_path)]
                for file in file_list:
                    #upload resource file
                    local_resource = (os.path.join(mni_mat_file_path, file))
                    fileName = file

                    # print("Uploading subject resource... ", local_resource)
                    resource.file(fileName).insert(local_resource)


                file_list = [name for name in os.listdir(data_file_path)]
                num_subjects = len(file_list)
                print("Creating and uploading data for {subjects} subjects".format(subjects=num_subjects+1))
                
                i = 1
                for file in file_list:
                    #formatting subject name 

                    # subject name just an integer 
                    # subject_name = "subject_"+str(i)

                    #subject name with file type
                    type = file.split('_')[-2]
                    subject_name = "participant_"+str(i)+"_"+type
                    # print(subject_name)

                    print("Creating subject... ", subject_name)
                    subject = my_project.subject(subject_name)
                    #create subject
                    subject.create()

                    #create resource
                    resource = subject.resource('data_sample')
                    if not resource.exists():
                        resource.create()

                    #upload resource file
                    local_resource = (os.path.join(data_file_path, file))
                    fileName = "participant_"+type+".mat"

                    # print("Uploading subject resource... ", local_resource)
                    resource.file(fileName).insert(local_resource)
                    resource.file('params.txt').insert(params_file_path)

                    i = i+1



                #creating subject with multiple data sets 
                subject_name = "subject_"+ str(i) +"_multiple"
                print("Creating subject... ", subject_name)
                subject = my_project.subject(subject_name)
                # create subject
                subject.create()

                # create resource
                resource = subject.resource('data_sample')
                if not resource.exists():
                    resource.create()

                for file in file_list:
                    # upload resource file
                    local_resource = (os.path.join(data_file_path, file))

                    # create resource
                    file_type = file.split('_')[-2]
                    fileName = "subjectdata_" + file_type + ".mat"
                    # print("Uploading subject resource... ", local_resource)
                    resource.file(fileName).insert(local_resource)
                resource.file('params.txt').insert(params_file_path)
                resource.file('params2.txt').insert(params_file_path2)

                print("Data has finished uploading")
            else: 
                print("Project ", project_name, " already exists adding user to their project")
                member_url = xnat_url + "/data/projects/{project}/users/{project}_member/{username}".format(project=project_name, username=user)
                r = s.put(member_url)
                print("Added ", user, " to project ", project_name, "\n", r)
            new_users_projects_created.append(str(user))
# close connection
print("new projects created for users: \n")
print(new_users_projects_created)
interface.disconnect()
s.post(xnat_url+"/app/action/LogoutUser")
