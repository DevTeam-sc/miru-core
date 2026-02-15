import sys

sys.path.insert(0, "/Users/oleavr/src/miru/build/miru-macos-universal/lib/python2.7/site-packages")

if __name__ == "__main__":
    from PyObjCTools import AppHelper

    AppHelper.runEventLoop()
