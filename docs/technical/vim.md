# Vim

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Vim Tutorial for Beginners - Complete Course**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=IiwGbcd8S7I)
- **Why it's great**: Comprehensive introduction to Vim with practical examples and hands-on exercises

#### **Mastering Vim Quickly**
- **Channel**: Thoughtbot
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=wlR5gYd6um0)
- **Why it's great**: Focused approach to learning essential Vim commands and workflows

#### **Vim as IDE - Complete Tutorial**
- **Channel**: ThePrimeagen
- **Link**: [YouTube - 2 hours](https://www.youtube.com/watch?v=ctH-a-1eUME)
- **Why it's great**: Advanced Vim usage with plugins and IDE-like functionality

### 📖 Essential Documentation

#### **Vim Official Documentation**
- **Link**: [vimhelp.org](https://vimhelp.org/)
- **Why it's great**: Complete official documentation with searchable help system

#### **Vim User Manual**
- **Link**: [vimdoc.sourceforge.net/htmldoc/usr_toc.html](http://vimdoc.sourceforge.net/htmldoc/usr_toc.html)
- **Why it's great**: Structured learning path from basics to advanced features

#### **Vim Reference Manual**
- **Link**: [vimdoc.sourceforge.net/htmldoc/help.html](http://vimdoc.sourceforge.net/htmldoc/help.html)
- **Why it's great**: Comprehensive reference for all Vim commands and options

### 📝 Must-Read Blogs & Articles

#### **Practical Vim Tips**
- **Source**: Vim Tips Wiki
- **Link**: [vim.fandom.com/wiki/Vim_Tips_Wiki](https://vim.fandom.com/wiki/Vim_Tips_Wiki)
- **Why it's great**: Community-driven collection of practical tips and tricks

#### **Learn Vim Progressively**
- **Source**: Yann Esposito
- **Link**: [yannesposito.com/Scratch/en/blog/Learn-Vim-Progressively](http://yannesposito.com/Scratch/en/blog/Learn-Vim-Progressively/)
- **Why it's great**: Step-by-step approach to mastering Vim gradually

#### **Coming Home to Vim**
- **Source**: Steve Losh
- **Link**: [stevelosh.com/blog/2010/09/coming-home-to-vim](http://stevelosh.com/blog/2010/09/coming-home-to-vim/)
- **Why it's great**: Philosophical approach to understanding Vim's design and power

### 🎓 Structured Courses

#### **Practical Vim Book**
- **Platform**: Pragmatic Programmers
- **Link**: [pragprog.com/titles/dnvim2/practical-vim-second-edition](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
- **Cost**: Paid
- **Why it's great**: Comprehensive book with practical techniques and real-world examples

#### **Vim Masterclass**
- **Platform**: Udemy
- **Link**: [udemy.com/course/vim-commands-cheat-sheet](https://www.udemy.com/course/vim-commands-cheat-sheet/)
- **Cost**: Paid
- **Why it's great**: Structured course with exercises and practical applications

### 🛠️ Tools & Platforms

#### **Vim Adventures**
- **Link**: [vim-adventures.com](https://vim-adventures.com/)
- **Why it's great**: Interactive game to learn Vim commands in a fun way

#### **Vim Awesome**
- **Link**: [vimawesome.com](https://vimawesome.com/)
- **Why it's great**: Discover and explore Vim plugins with ratings and usage statistics

#### **OpenVim Interactive Tutorial**
- **Link**: [openvim.com](https://www.openvim.com/)
- **Why it's great**: Interactive browser-based Vim tutorial with hands-on practice

## Overview

Vim is a powerful, modal text editor that's essential for platform engineers working on remote servers and in terminal environments. It's highly configurable, efficient for text editing, and available on virtually every Unix-like system.

## Key Features

- **Modal Editing**: Different modes for navigation, editing, and commands
- **Highly Configurable**: Extensive customization through .vimrc
- **Powerful Navigation**: Efficient text navigation and manipulation
- **Plugin Ecosystem**: Rich ecosystem of plugins and extensions
- **Universal Availability**: Pre-installed on most Linux/Unix systems

## Basic Operations

### Modes
```bash
# Normal mode (default) - for navigation and commands
Esc  # Return to normal mode from any other mode

# Insert mode - for typing text
i    # Insert before cursor
a    # Insert after cursor
I    # Insert at beginning of line
A    # Insert at end of line
o    # Open new line below
O    # Open new line above

# Visual mode - for selecting text
v    # Character-wise selection
V    # Line-wise selection
Ctrl+v  # Block-wise selection

# Command mode - for running commands
:    # Enter command mode
```

### Navigation
```bash
# Basic movement
h, j, k, l  # Left, down, up, right
w           # Next word
b           # Previous word
e           # End of word
0           # Beginning of line
$           # End of line
gg          # Top of file
G           # Bottom of file

# Advanced navigation
f<char>     # Find character forward
F<char>     # Find character backward
t<char>     # Move to before character
/<pattern>  # Search forward
?<pattern>  # Search backward
n           # Next search result
N           # Previous search result
```

### Editing Commands
```bash
# Deletion
x     # Delete character under cursor
X     # Delete character before cursor
dd    # Delete entire line
dw    # Delete word
d$    # Delete to end of line
d0    # Delete to beginning of line

# Copy and paste
yy    # Copy (yank) line
yw    # Copy word
y$    # Copy to end of line
p     # Paste after cursor
P     # Paste before cursor

# Change/replace
cc    # Change entire line
cw    # Change word
r<char>  # Replace character
R     # Replace mode
s     # Substitute character
S     # Substitute line
```

## Configuration

### Basic .vimrc
```vim
" ~/.vimrc - Basic Vim configuration

" General settings
set number          " Show line numbers
set relativenumber  " Show relative line numbers
set ruler           " Show cursor position
set showcmd         " Show command in status line
set wildmenu        " Enhanced command completion
set hlsearch        " Highlight search results
set incsearch       " Incremental search
set ignorecase      " Case insensitive search
set smartcase       " Case sensitive if uppercase used

" Indentation
set autoindent      " Auto-indent new lines
set smartindent     " Smart auto-indenting
set expandtab       " Use spaces instead of tabs
set tabstop=4       " Tab width
set shiftwidth=4    " Indent width
set softtabstop=4   " Soft tab width

" Interface
set laststatus=2    " Always show status line
set cursorline      " Highlight current line
set colorscheme=desert  " Color scheme
syntax enable       " Enable syntax highlighting

" Key mappings
let mapleader = ","  " Set leader key
nnoremap <leader>w :w<CR>        " Quick save
nnoremap <leader>q :q<CR>        " Quick quit
nnoremap <leader>h :nohlsearch<CR> " Clear search highlight
```

### Platform Engineering Specific Configuration
```vim
" Platform engineering focused .vimrc

" File type detection
filetype plugin indent on

" YAML files (common in k8s, docker-compose)
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab
autocmd FileType yml setlocal ts=2 sts=2 sw=2 expandtab

" JSON files
autocmd FileType json setlocal ts=2 sts=2 sw=2 expandtab

" Shell scripts
autocmd FileType sh setlocal ts=4 sts=4 sw=4 expandtab

" Dockerfile
autocmd FileType dockerfile setlocal ts=4 sts=4 sw=4 expandtab

" Terraform
autocmd FileType terraform setlocal ts=2 sts=2 sw=2 expandtab

" Show whitespace
set listchars=tab:>·,trail:·,extends:>,precedes:<
set list

" Line length indicator
set colorcolumn=80

" Key mappings for common tasks
nnoremap <leader>e :e ~/.vimrc<CR>  " Edit vimrc
nnoremap <leader>r :source ~/.vimrc<CR>  " Reload vimrc
```

## Essential Commands

### File Operations
```bash
# Opening files
:e filename     # Edit file
:o filename     # Open file
:sp filename    # Split window horizontally
:vsp filename   # Split window vertically

# Saving and quitting
:w              # Save
:w filename     # Save as
:q              # Quit
:q!             # Quit without saving
:wq or :x       # Save and quit
:wa             # Save all
:qa             # Quit all
```

### Search and Replace
```bash
# Search
/pattern        # Search forward
?pattern        # Search backward
n               # Next occurrence
N               # Previous occurrence

# Replace
:s/old/new/     # Replace first occurrence in line
:s/old/new/g    # Replace all in line
:%s/old/new/g   # Replace all in file
:%s/old/new/gc  # Replace all with confirmation
```

### Working with Multiple Files
```bash
# Buffers
:ls             # List buffers
:b2             # Switch to buffer 2
:bn             # Next buffer
:bp             # Previous buffer
:bd             # Delete buffer

# Windows
Ctrl+w s        # Split horizontally
Ctrl+w v        # Split vertically
Ctrl+w w        # Switch windows
Ctrl+w q        # Close window
Ctrl+w =        # Equal window sizes
```

## Useful Plugins for Platform Engineers

### Plugin Manager (vim-plug)
```vim
" Add to .vimrc
call plug#begin('~/.vim/plugged')

" Essential plugins
Plug 'preservim/nerdtree'          " File explorer
Plug 'vim-airline/vim-airline'     " Status line
Plug 'tpope/vim-fugitive'          " Git integration
Plug 'airblade/vim-gitgutter'      " Git diff in gutter
Plug 'hashivim/vim-terraform'      " Terraform syntax
Plug 'pearofducks/ansible-vim'     " Ansible syntax
Plug 'ekalinin/Dockerfile.vim'     " Dockerfile syntax
Plug 'stephpy/vim-yaml'            " Better YAML support

call plug#end()
```

### Key Plugin Commands
```bash
# NERDTree (file explorer)
:NERDTree       # Open file tree
Ctrl+n          # Toggle NERDTree (with mapping)

# Git (vim-fugitive)
:Git status     # Git status
:Git add %      # Add current file
:Git commit     # Commit
:Git push       # Push
:Git blame      # Git blame
```

## Advanced Techniques

### Macros
```bash
# Record and play macros
qa              # Start recording macro 'a'
<commands>      # Perform actions
q               # Stop recording
@a              # Play macro 'a'
@@              # Repeat last macro
5@a             # Play macro 'a' 5 times
```

### Text Objects
```bash
# Common text objects
ciw             # Change inner word
caw             # Change a word
ci"             # Change inside quotes
ca"             # Change around quotes
cit             # Change inside HTML tag
dap             # Delete a paragraph
yip             # Yank inner paragraph
```

### Registers
```bash
# Named registers
"ayy            # Yank line to register 'a'
"ap             # Paste from register 'a'
:reg            # Show all registers

# System clipboard
"+yy            # Yank to system clipboard
"+p             # Paste from system clipboard
```

## Best Practices

- Learn modal editing philosophy - stay in normal mode
- Use relative line numbers for efficient navigation
- Master text objects for efficient editing
- Create custom key mappings for frequent operations
- Use plugins judiciously - start minimal and add as needed
- Practice regularly to build muscle memory
- Learn one new command/technique per week

## Great Resources

- [Vim Documentation](https://vimhelp.org/) - Official comprehensive documentation
- [Vim Adventures](https://vim-adventures.com/) - Interactive game to learn Vim
- [vimtutor](https://www.openvim.com/) - Built-in Vim tutorial (run `vimtutor` in terminal)
- [Vim Awesome](https://vimawesome.com/) - Discover and install Vim plugins
- [Practical Vim Book](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/) - Comprehensive Vim guide
- [Vim Golf](https://www.vimgolf.com/) - Solve editing challenges efficiently
- [vim.fandom.com](https://vim.fandom.com/wiki/Vim_Tips_Wiki) - Community tips and tricks