;; .oO (c) DOP (dohmatob elvis dopgima) Oo.
;; THIS IS MY EVER-CHANGING DOTEMACS FILE!!

;; ++++
;; MISC
;; ++++ 

; Start maximized
;; XXX remove X-term dependence and ignore function if already in maximized mode!!!
(defun toggle-maximized ()
  (interactive)
  (x-send-client-message nil 0 nil "_NET_WM_STATE" 32
                         '(2 "_NET_WM_STATE_MAXIMIZED_VERT" 0))
  (x-send-client-message nil 0 nil "_NET_WM_STATE" 32
                         '(2 "_NET_WM_STATE_MAXIMIZED_HORZ" 0))
)
; (toggle-maximized)

; Enable line-numbering
(global-linum-mode 1)

; Highlight current line
; (global-hl-line-mode 1)

; Highlight matching parenthesis
(show-paren-mode 1)

;; +++++++++++
;; COLOR-THEME
;; +++++++++++
; Load color-theme
(add-to-list 'load-path
	     "/usr/share/emacs23/site-lisp/emacs-goodies-el")
(require 'color-theme)
(color-theme-select)
(color-theme-tty-dark)

;; END // MISC

;; ++++++++++++++++++
;; AUTO COMPLETE MODE
;; ++++++++++++++++++

; XXX You'll need to download and install "auto complete mode"; then replace the follow by the spat-out output 
(add-to-list 'load-path 
	     "~/.emacs.d/")
(require 'auto-complete-config)
(add-to-list 'ac-dictionary-directories "~/.emacs.d//ac-dict")
(ac-config-default)

;; END // AUTO COMPLETE MODE

; ;; +++++++++++
; ;; NXHTML-MODE
; ;; +++++++++++
; (load "~/.emacs.d/nxhtml/autostart.el")

;; ++++++++++++++
;; FLYMAKE & PEP8
;; ++++++++++++++
(add-to-list 'load-path "~/.emacs.d")
(add-hook 'python-mode-hook 'flymake-find-file-hook)
(when (load "flymake" t)
  (defun flymake-pyflakes-init ()
    (let* ((temp-file (flymake-init-create-temp-buffer-copy
               'flymake-create-temp-inplace))
       (local-file (file-relative-name
            temp-file
            (file-name-directory buffer-file-name))))
      (list "pycheckers.sh"  (list local-file))))
   (add-to-list 'flymake-allowed-file-name-masks
             '("\\.py\\'" flymake-pyflakes-init)))
(load-library "flymake-cursor")
(global-set-key [f10] 'flymake-goto-prev-error)
(global-set-key [f11] 'flymake-goto-next-error)

;; END // FLYMAKE AND PEP8

;; +++++
;; CEDET
;; +++++

; Load CEDET
(load-file "~/.emacs.d/cedet-1.1/common/cedet.el")

(global-ede-mode t)
(semantic-load-enable-excessive-code-helpers)
(require 'semantic-ia)
(require 'semantic-gcc)
(semantic-add-system-include "/usr/include/boost" 'c++-mode)
(setq-mode-local c-mode semanticdb-find-default-throttle
                 '(project unloaded system recursive)) ; extract syntactic information when Emacs is idle

; Integration with imenu
(defun my-semantic-hook ()
  (imenu-add-to-menubar "TAGS"))
(add-hook 'semantic-init-hooks 'my-semantic-hook)

; customization of semanticdb
(require 'semanticdb)
(global-semanticdb-minor-mode 1)

;; if you want to enable support for gnu global
(when (cedet-gnu-global-version-check t)
  (require 'semanticdb-global)
  (semanticdb-enable-gnu-global-databases 'c-mode)
  (semanticdb-enable-gnu-global-databases 'c++-mode))

;; enable ctags for some languages:
;;  Unix Shell, Perl, Pascal, Tcl, Fortran, Asm
(when (cedet-ectag-version-check)
  (semantic-load-enable-primary-exuberent-ctags-support))

; turn-on source code folding/unfolding feature
(global-semantic-tag-folding-mode)

;; END // CEDET

;; +++
;; ECB
;; +++

; Load ECB (Emacs Code Browser)
(add-to-list 'load-path
	     "~/.emacs.d/ecb-2.40")
(require 'ecb)
(require 'ecb-autoloads)

; Disable tip-of-the-day crap
(setq ecb-tip-of-the-day nil)
(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(ecb-options-version "2.40"))
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )

;; END // ECB

;; Trick to be able to use french <<accent circonflexe>>
(load-library "iso-transl")

;; Trick to (auto) reload all buffers when a file changes on disk, etc.
;; src: http://stackoverflow.com/questions/1480572/how-to-have-emacs-auto-refresh-all-buffers-when-files-have-changed-on-disk
(global-auto-revert-mode t)

;; Declare the flyspell-mode function as auto-load
(autoload 'flyspell-mode "flyspell" "On-the-fly spelling checker." t)
;; Automate the starting of flyspell when editing LaTeX source files
(add-hook 'LaTeX-mode-hook 'flyspell-mode)

;; E.O.F.
