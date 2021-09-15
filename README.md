## Hapy - Write Python in Hausa!
### version 0.0.1
hausa-python to english-python translator thingy

Emmanuel Segun-Lean (undergrad final project)

thank you Jesus!

### aim:

Should be able to take a file or string like:
> Let's say 'kira' is define in Hausa and 'buga' is the word for print.
```python
    # wannan sharhi ne
    kira muje(){
        buga("Gooooooo")
    }

    muje()
```
and produce correct python code that is executable

```python
    # wannan sharhi ne
    def muje():
        print("Goooooo")

    muje()
    >>> "Goooooo"
```

### method
 At first I am starting by doing a simple python dialect that is almost exactly the same expect that we support bracket blocks instead of indented blocks and keywords etc are in hausa :] 

 > if { *expressions* } -> if: *expressions*

 The plan:

 | Completed? | Aspect | Status |
| ------------ | ------------- | ----------- |
|:white_large_square: | Develop language that compiles to python and is executable | in progress :hourglass: |
| :white_large_square: | Write documentation | pending :date: |
| :white_large_square: | Make online learning platform and other supporting things e.g editor support, CI/CD stuff | pending :date: |



### credits

- (heavily) inspired by this great, easy-to-follow [tutorial](https://lisperator.net/pltut)