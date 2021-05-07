# shellbinscript

Utility to create a shell script embedding a directory inside the script.
If a run.sh script is present in the input directory it will be executed.

Using this utility you can create simple installers.

## Usage

```
shellbinscript.py [-h] inputdir outfile
```

### Example

To create an installer with some files that have to be copied:

```
[shellbinscript]$ find installer/
installer/
installer/run.sh
installer/file_a.dat
installer/file_b


[shellbinscript]$ cat installer/run.sh
set -x
echo "running the installer"

cp file_a.dat /usr/lib/file_a.dat
cp file_b /usr/sbin/file_b

echo "doing more stuff"
chmod +x /usr/sbin/file_b

[shellbinscript]$ shellbinscript.py installer/ myinstaller.sh
```

## License

Licensed under the Apache 2.0 license.
