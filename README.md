# Batch mv(1) multiple (old filename, new filename) pairs without overwriting anything

## Introduction

`mv(1)` is a handy command that rename one file to another.
However, the problem is that the `another` file will get overlapped.
`mv(1)`, in that case, provides the users with an `-i` option so that the `another` file won't be overwritten (and so that the command won't move anything).

Nevertheless, there exist cases where a collection of files will be renamed in such a faulty way that some files overwrite other files.
For example, if we want to rename from `A` to `B`, and `B` to `C`.
The trivial options are: `mv A B; mv B C`, or `mv -i A B; mv -i B C`.
The first option slays both `B` and `C`, and renders `C` the `A`'s content; whereas the second option stops the first command from overwriting and successfully `mv B C`.
A slightly smart option is this: `mv B C; mv A B`, such that no file will be overwritten.
Here we don't consider the harder case, say `mv A B; mv B A`, requiring one temporary file, due to its complexity.

## batchmv comes into rescue

`batchmv` uses under the case `os.rename(src, dst)` to rename files.
But it is slightly smarter to rearrange the renaming order so as to avoid overwriting from happening.
Sadly the harder case where temporary files is required cannot be solved.


## How to use `batchmv`

It's really simple to use.
Just read the docstring in [`batchmv.py`](https://github.com/kkew3/pybatchmv/blob/main/batchmv/batchmv.py)
