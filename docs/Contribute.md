# **Guide to get going with this repo**

## Development environment

### **Install VSCode**
VSCode is our preferred code editor/IDE as it is _free_, well documented and modular. We can therefore tailor our needs on the specific project. Although other IDEs can be used (Pycharm, IDLE etc.) VSCode is strongly recommended.
1. Install [VSCode]()
with the following extensions
    * [Remote Container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
    * [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) (Windows only)
    * [Remote WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) (Windows only)


### **Open repo in devcointainer**
_Devcontainers_ are a way to isolate and replicate development environments through VSCode. The main benefints are that host-system (your laptop) remains unaffected by any misconfigurations/installations. Further developoing inside the _devcontainer_  ensures that one can specify exact dependecies such as OS, python version, environment variables across all contributers to a repo.

1. **Enable WSL2 (Windows only)**
    1. Verify if WSL2 is installed
        On your machine by opening command prompt (cmd) and type the following
        ```cmd
        $ wsl -l -v
        NAME                   STATE           VERSION
        Ubuntu-20.04           Running         2
        ```
        If ```wsl -l -v``` output anything other than the above, proceed with installation of WSL2, else skip to **installation of Docker**

    2. Follow the steps under _Manual installation_ [microsoft.com/enable-wsl2](https://docs.microsoft.com/en-us/windows/wsl/install-win10#manual-installation-steps)
        1. It is very important to follow all mandatory steps in correct order.

        2. Remember to set Windows to use WSL2 as default by running
            ```cmd
            $ wsl --set-default-version 2
            For information on key differences with WSL 2 please visit https://aka.ms/wsl2
            The operation completed successfully.
            ```
        3. Please confer with the trouble shooting guide if any issues: [microsoft.com/troubleshooting installation](https://docs.microsoft.com/en-us/windows/wsl/install-win10#troubleshooting-installation)
        4. Run ```wsl -l -v``` to verify the installation.
2. **Install docker-desktop**
Docker utlizes WSL2 as backend on Windows hosts :-)
    1. If you already have ```docker-desktop``` make sure version is ```>= 4.0.1```. Else proceeed to the next step.
    2. Go to to docker.com/products/docker-desktop and download docker-desktop and install
        1. [Mac installation steps](https://docs.docker.com/desktop/mac/install/)
        2. [Windows installation steps](https://docs.docker.com/desktop/windows/install/)

3. **Clone repo**
    **Mac users**
    1. Open _terminal_ and type:
     ```zsh
     git clone https://github.com/acntech/data-driven-fpl.git
    ```
    **Windows users**
    1. Open VSCode
    2. Go to the _Remote explorer_ found in the left sidebar
    3. From the _dropdown_ select _WSL targets_
    4. Find the  _Ubuntu 20.04 distro_ and right-click _open folder in WSL_
    5. Open the VSCode integrated terminal ```CTRL+Shift+Ø``` and type:
        ```bash
        git clone https://github.com/acntech/data-driven-fpl.git
        ```

    *_A more comprahensive VSCode+WSL guide can be found at [visualstudio.com/wsl-tutorial](https://code.visualstudio.com/docs/remote/wsl-tutorial)_

4. **Open repository in devcontainer**
    1. In VSCode repoen the cloned repo by selecting: File -> Open folder -> \<CLONED FOLDER ROOTDIR\>
    2. Open the folder in _devcontainer_ by:
        1. Responding to the automatic prompt when VSCode detects the presence of ```.devcontainer``` dir
        2. Open VSCode command-pallet by pressing ```Ctrl+Shift+P``` or ```Cmd + Shift + P``` for Mac and type:
            ```cmd
            remote-containers.rebuildAndReopenInContainer
            ```
        3. Observe that the container is built and reopened in a new Window.
        4. VSCode must reload and thus container must be reopened for remote extensions to take effect
    *_A more comprehensive VSCode+devcontainer guide can be found at [visualstudio.com/devcontainer](https://code.visualstudio.com/docs/remote/containers)

### **Open repo at remote-ssh host (Virtualbox or Cloud instance)**
Remote SSH enables users to work on the code on a virtual machine such as the Virtualbox/Vagrant setup we have created here -> [vagrant-ml-developer](https://github.com/acntech/vagrant-ml-developer) or on Cloud VM instances! A more comprehensive guide on _remote SSH_ can be found here [vscode.com/remote-ssh](https://code.visualstudio.com/docs/remote/ssh). A key difference between _remote ssh_ and _devcontainer_ is that the source code is **only** stored on the remote instance.

1. **Virtualbox + Vagrant**
    1. Make sure that you have Virtualbox and Vagrant installed if not please consider to
    [open repo in devcointainer](#open-repo-in-devcointainer)
    2. Create a directory on your Windows host. Name the directory ml-developer
    3. Copy the following ```Vagrantfile``` into the directory [github.com/acntech/vagrant-ml-developer](https://raw.githubusercontent.com/acntech/vagrant-ml-developer/develop/machines/ml_developer-minimal_example_machine/Vagrantfile)
    4. Make sure that the ```Vagrantfile``` only reference the new version of ```acntech/ml-developer-minimal``` as it should be downloaded from Vagrantcloud and **NOT** built locally.
    5. Open _command prompt_ Navigate to the directory holding the ````Vagrantfile``` and type:
        ```cmd
        vagrant up
        ```
2. **Connect to remote host in VSCode**
    1. Open _Remote explorer_ from the left sidebar
    2. From the _dropdown_ select _SSH Targets_
    3. Configure SSH remote environment by:
        1. Remote Explorer -> Configure -> ```C:\Users\<USER>\.ssh\config```
        2. Add following configuration:
            ```cmd
            Host <INSERT DESIRED MACHINE NAME>
                HostName 127.0.0.1
                Port 2222
                User vagrant
                IdentityFile <PATH TO VAGRANT FOLDER>\.vagrant\machines\default\virtualbox\private_key
            ```
    4. Right-click the desired machine in the Remote Explorer and select _Open on SSH host in new window_
    5. Verify that VSCode connects and opens the _remote SSH_ machine. If prompted type ```vagrant``` as password.
    6. Trouble shooting tips:
        1. Sometimes Remote targets with same address are used (for example 127.0.0.1:2222) when working with Virtualbox. Then the ```C:\Users\<USER>\.ssh\known_hosts``` must be cleared as SSH fingerprint changes.
3. **Clone repo on remote host**
    1. Once connected to the remote host type:
    ```bash
    git clone https://github.com/acntech/data-driven-fpl.git
    ```
    2. In VSCode select File -> Open folder -> \<CLONED FOLDER ROOTDIR\> to reopen the remote host inside the repo.