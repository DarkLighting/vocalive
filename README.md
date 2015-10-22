**Live Vocabulary Observer**

```
usage: vocalive.py [-h] [-m Length] [-o File] Address

Live Vocabulary Observer

positional arguments:
  Address               Web address to learn from

optional arguments:
  -h, --help            show this help message and exit
  -m Length             Word minimum length. Default = 2
  -o File, --output File
                        File to save learned words

```

This tool creates a dictionary using the words found at the specified web address. Let's say you wanted to make a list of all the unique words present in an html page. All you have to do is run:

```
./vocalive.py -o out_file.txt http://blog.example.com
```
It will create a file named "out_file.txt" in the same folder containing the unique words found in blog.example.com web page. You may specify the minimum length of words using the ```-m``` parameter. If you don't set that, the default length is 2 characters.


**Feature requests are very welcome!**<br>
Please start a new issue on the top right corner of the screen for better organization.
