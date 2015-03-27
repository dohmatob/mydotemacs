This is my emacs configuration.

Installation
------------

Installing dependencies
=======================
To install all other dependencies, simply run apt-get from the command-line as follows:
  
  $ apt-get remove emacs24
  
  $ apt-get install emacs23 emacs-goodies-el pylint pep8 exuberant-ctags

For best results, I recommend using emacs23, and not emacs24 (uninstalled as above, if present!).
Installing mydotemacs
=====================
- Copy .emacs file to your home directory (~);
- Copy .emacs.d directory to your home directory (~). If you already have a ~/.emacs.d directory, then copy the contents (files and subdirectories) of .emacs.d there.
- Copy pycheckers.sh to your home directory (~).
- Copy epylint.py to your home directory (~).
- Finally, add the following line (necessary for flymake/pep8 to work properly) at the end of your ~/.bashrc file:
  
  $ export PATH=$PATH:~	     

New features 12th June 2014
---------------------------
My own epylint.py to avoid abnoxious pylint warnings (like: Module 'numpy' has no 'dot' member ..., etc.)

BUGS
----
Send bug reports to me at: gmdopp@gmail.com or elvis.dohmatob@inria.fr

That's all!
-DOP/ELVIS/SOLO
