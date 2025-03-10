# Dependencies  

- Python3
- PyGObject
- Python-Nautilus
- Nautilus

# Installation

##### 1. Let's clone the repo and change the directory:

```
git clone https://github.com/ivan-mitriakhin/nautilus-image-actions.git

cd /nautilus-image-actions
```
 
##### 2. Install all the required dependencies based on your system (you may refer to the following [link](https://pygobject.gnome.org/getting_started.html#ubuntu-logo-ubuntu-debian-logo-debian)):

- ##### Ubuntu / Debian

```
sudo apt install libcairo2-dev pkg-config python3-dev python3-gi \
            python3-gi-cairo gir1.2-gtk-4.0 python3-nautilus
```

- ##### Fedora

```
sudo dnf install gcc gobject-introspection-devel cairo-gobject-devel \
            pkg-config python3-devel gtk4 nautilus-python
```

##### 3. Install the required python libriares:

```
pip3 install -U pip

pip3 install -r requirements.txt
```

##### 4. Run the bash script:

```
sh ./run.sh
```