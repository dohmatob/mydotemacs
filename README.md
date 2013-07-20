This is my emacs configuration.

Usage
-----
- copy .emacs file to your home directory (~);
- copy .emacs.d directory to your home directory (~). If you already have a ~/.emacs.d directory, then copy the contents (files and subdirectories) of .emacs.d there.
- copy pycheckers.sh to your home directory (~), and render it executable (by running "chmod u+x ~/pycheckers.sh", for example)
- add the following line (necessary for flymake/pep8 to work properly) at the end of your ~/.bashrc file:
export PATH=$PATH:~

Installing dependencies
-----------------------
To install all other dependencies, simply run apt-get from the command-line as follows:
apt-get install emacs-goodies-el pylint pep8 exuberant-ctags

BUGS
----
Send bug reports to me at: elvis.dohmatob@inria.fr

That's all!
-DOP/ELVIS/SOLO
