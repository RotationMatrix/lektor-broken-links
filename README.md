# Broken Links

*Find all the broken links!*

Broken Links trys to help you detect broken links in your [Lektor](https://www.getlektor.com/) site.

Currently it's only smart enough to check internal links, but it's considering getting a degree in external link detection.

## Getting Started

Broken Links depends on the following packages...
* `markdown-it-py -= 0.4.5`
* `click -= 7.0`
* `furl -= 2.1.0`

...which can be easily installed with...

```
$ pip install markdown-it-py click furl
```

Once dependencies are installed, you can add Broken Links to your Lektor project with...

```
$ lektor plugins add lektor-broken-links
```

Alternatively Broken Links can be installed manually by copying the plugin folder into `packages/`.

Once Broken Links is installed, run `lektor build` or `lektor server`. Any broken internal links will be printed in the build output, along with the page they were found on.

```
broken-links-tests$ lektor build
Started build
Started link check
Found 2 broken links in '/':
    /none
    ./none
Found 1 broken link in '/nested':
    ../none
Finished link check in 0.02 sec
Finished build in 0.03 sec
Started prune
Finished prune in 0.00 sec
```
*Example output from building [the test site](https://github.com/RotationMatrix/broken-links-tests).*
