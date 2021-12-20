# Broken Links

*Find all the broken links!*

Broken Links helps you detect broken links in your [Lektor](https://www.getlektor.com/) site. It will warn you about broken internal and external HTTP links.

## Goals

- Fast - Less than 1 second to check sites with hundreds of pages.
- Simple - Install on your site and it quietly runs on every build.

## Getting Started

Broken Links depends on the following packages...
* `mistune >= 0.7.0, <2`
* `click >= 7.0`
* `furl >= 2.1.0`

...which can be easily installed with...

```
$ pip install mistune click furl
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
*Example output from building [the test site](https://github.com/RotationMatrix/lektor-broken-links-tests).*

## Contributing

Thank you for your interest in this project! If you find a bug or have an idea for an awesome new feature please open an issue.
Pull Requests which help close issues are welcome!
