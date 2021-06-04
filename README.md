[![Netlify Status](https://api.netlify.com/api/v1/badges/950c7b47-1f4a-4fa2-8440-81a131583699/deploy-status)](https://app.netlify.com/sites/wieting-one-click-cms/deploys)

# wieting-one-click-hugo-cms: Published on Netlify.com with NetlifyCMS 

This repository and subsequent static website were created on 2021-Jun-03 using [NetlifyCMS: Start with a Template](https://www.netlifycms.org/docs/start-with-a-template/) in a manner similar to what's documented in my blog at [Moving to Netlify CMS](https://blog.summittdweller.com/posts/2021/04/moving-to-netlify-cms/). Unfortunately, the _Wieting Theatre_ work that's mentioned in [that blog post](https://blog.summittdweller.com/posts/2021/04/moving-to-netlify-cms/) had to be destroyed after my _git_ repo was apparently corrupted.  [This remote](https://github.com/SummittDweller/wieting-one-click-hugo-cms) is a replacment for that earlier work.

## Hugo Site Starter

Like my previous _Netlify_ build, this project once again uses the [Deploy to Netlify](https://app.netlify.com/start/deploy?repository=https://github.com/netlify-templates/one-click-hugo-cms&stack=cms) button corresponding with the _Hugo Site Starter_ section of [NetlifyCMS: Start with a Template](https://www.netlifycms.org/docs/start-with-a-template/).  

## wieting-theatre-DO: Now a Git Subtree

The `site` portion of this project used to be just that, a subdirectory in a larger project built using the aforementioned _Hugo Site Starter_.  That `site` directory was spun from my original repo to create a new one, [wieting-theatre-DO](https://github.com/SummittDweller/wieting-theatre-DO), and that _git_ project is now a _git_ "subtree" inside the `site` directory here in [this remote](https://github.com/SummittDweller/wieting-one-click-hugo-cms).

I used guidance posted in [git subtrees: a tutorial](https://medium.com/@v/git-subtrees-a-tutorial-6ff568381844) to build the `site` directory out.  Specifics of the _git_ command stream I used are posted in raw form below:

```
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹empty-site›
╰─$ git checkout -b wieting-site-added
Switched to a new branch 'wieting-site-added'
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git remote add wieting-site git@github.com:SummittDweller/wieting-theatre-DO
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git subtree add --prefix=site/ wieting-site main
prefix 'site' already exists.
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ rm -fr site                   
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git subtree add --prefix=site/ wieting-site main
git fetch wieting-site main
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git remote add wieting-site https://github.com/SummittDweller/wieting-theatre-DO   
fatal: remote wieting-site already exists.
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git remote add wieting-theatre-DO https://github.com/SummittDweller/wieting-theatre-DO 
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
╰─$ git subtree add --prefix=site/ wieting-theatre-DO main
git fetch wieting-theatre-DO main
warning: no common commits
remote: Enumerating objects: 370, done.
remote: Counting objects: 100% (370/370), done.
remote: Compressing objects: 100% (310/310), done.
remote: Total 370 (delta 48), reused 364 (delta 42), pack-reused 0
Receiving objects: 100% (370/370), 19.52 MiB | 13.64 MiB/s, done.
Resolving deltas: 100% (48/48), done.
From https://github.com/SummittDweller/wieting-theatre-DO
 * branch            main       -> FETCH_HEAD
 * [new branch]      main       -> wieting-theatre-DO/main
Added dir 'site'
╭─mark@Marks-Mac-Mini ~/GitHub/wieting-one-click-hugo-cms ‹wieting-site-added›
```

Be sure to note the trial-and-error (emphasis on _error_) in that sequence. Once I had it working locally I pushed the _wieting-site-added_ branch of the code and merged it with _main_ for publication.

## Bringing Updates from _my-subproject_ Back to Parent

The heading of this section, above, also appears as a heading in the [guidance post](https://medium.com/@v/git-subtrees-a-tutorial-6ff568381844) that I used here for subtree creation.  In that post _my-subproject_ is the name of the _git_ remote that the author incorporated as a subtree.  In my case, the _git_ remote name, or alias, is _wieting-theatre-DO_ and it was successfully created after some failed attempts using this command: `$ git remote add wieting-theatre-DO https://github.com/SummittDweller/wieting-theatre-DO`, as you see above.

That remote repo was subseuqently added into the `site/` subdirectory as a subtree using: `$ git subtree add --prefix=site/ wieting-theatre-DO main`.

The author of the post says "_Imagine that someone made awesome contributions to my-subproject and you want to pull these new changes back into parent_", and proceeds to show us how that can be done. The process is elegantly simple, and one that I hope to repeat in my _project/sub-project_ arrangement.  The author's command, "git subtree pull --prefix=vendor my-subtree master", becomes `git subtree pull --prefix=site wieting-theatre-DO main`, in my case.  

The author goes on to says that... "_This will execute a pull, using the “subtree” merge strategy. It is necessary so we tell git to inspect the patches and identify it should be applying in a subtree of our current project (parent)..._" and that "_This will generate a merge commit..._"  Later, the author also suggests using the `--squash` flag as part of the `git subtree pull...` command so my preferred syntax should probably be: `git subtree pull --prefix=site --squash wieting-theatre-DO main`. 


 


# Hugo template for Netlify CMS with Netlify Identity

This is a small business template built with [Victor Hugo](https://github.com/netlify/victor-hugo) and [Netlify CMS](https://github.com/netlify/netlify-cms), designed and developed by [Darin Dimitroff](http://www.darindimitroff.com/), [spacefarm.digital](https://www.spacefarm.digital).

## Getting started

Use our deploy button to get your own copy of the repository. 

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/netlify-templates/one-click-hugo-cms&stack=cms)

This will setup everything needed for running the CMS:

* A new repository in your GitHub account with the code
* Full Continuous Deployment to Netlify's global CDN network
* Control users and access with Netlify Identity
* Manage content with Netlify CMS

Once the initial build finishes, you can invite yourself as a user. Go to the Identity tab in your new site, click "Invite" and send yourself an invite.

Now you're all set, and you can start editing content!

## Local Development

Clone this repository, and run `yarn` or `npm install` from the new folder to install all required dependencies.

Then start the development server with `yarn start` or `npm start`.

## Layouts

The template is based on small, content-agnostic partials that can be mixed and matched. The pre-built pages showcase just a few of the possible combinations. Refer to the `site/layouts/partials` folder for all available partials.

Use Hugo’s `dict` functionality to feed content into partials and avoid repeating yourself and creating discrepancies.

## CSS

The template uses a custom fork of Tachyons and PostCSS with cssnext and cssnano. To customize the template for your brand, refer to `src/css/imports/_variables.css` where most of the important global variables like colors and spacing are stored.

## SVG

All SVG icons stored in `site/static/img/icons` are automatically optimized with SVGO (gulp-svgmin) and concatenated into a single SVG sprite stored as a a partial called `svg.html`. Make sure you use consistent icons in terms of viewport and art direction for optimal results. Refer to an SVG via the `<use>` tag like so:

```
<svg width="16px" height="16px" class="db">
  <use xlink:href="#SVG-ID"></use>
</svg>
```
