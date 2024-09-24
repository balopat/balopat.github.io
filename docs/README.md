# balintpato.com blog

The theme is cloned from[gregorygundersen.com/blog](http://gregorygundersen.com/blog/). For details, see [this post](http://gregorygundersen.com/blog/2020/06/21/blog-theme).
Huge thank you to Gregory for the simple, minimalistic, working blog template! 


## Setup / Running 

This is still using a bit of an old jekyll, so you'll have to install with these instructions: 

1. Install rvm (https://rvm.io/rvm/install)
2. Install Ruby 2.x and Bundler
```
rvm pkg install openssl
rvm reinstall ruby-2 --with-openssl-dir=$rvm_path/usr
gem install bundler -v 2.4.22
```
3. Run by:

```
bundle exec jekyll serve 
```
4. To include drafts 
```
bundle exec jekyll serve --drafts
```

## Build / publish

I use the docs folder with Github pages, so run this before committing and `git push`:

```
bundle exec jekyll build -d docs
```
