# Flatpak Metadata for PySolFC (WIP)

A Flatpak packaging setup for [PySolFC](https://pysolfc.sourceforge.io/) that
should be ready for submission.

## Additional "Nice to Have" Ideas

1. Check if Tkinter requires any of the `.tcl` files in `/lib` or if we can add
   them to `cleanup` to reduce the package size.
2. Replace `0001-allow-app-paths.patch` with a proper upstream fix to have
   PyGame derive the install prefix from its location rather than hard-coding
   the list of places to look for assets.
3. Contact skomoroh for permission to relicense the rest of the release
   announcements for inclusion in the Appstream XML file.
4. Clean up staleness in PySol's build instructions and deduplicate build
   automation as noticed in
   [this comment](https://github.com/shlomif/PySolFC/issues/256#issuecomment-1242955493).
   (May want to setup some `Vagrantfile`s to automate spinning up the various
   distros and installing PySolFC to identify staleness in the dependency
   installation commands given in the README.)
5. Convert `take_screenshot.py` from a proof of concept to a proper tool.
6. Contribute a Flatpak theme package for the GTK+ 2.x version of Breeze to
   Flathub (it'd also benefit apps like
   [Geeqie](https://flathub.org/apps/details/org.geeqie.Geeqie)) and then try
   adding [gtkTtk](https://github.com/Geballin/gtkTtk) as PySolFC's default Ttk
   theme... possibly through
   [python-gttk](https://github.com/TkinterEP/python-gttk)
7. Port the experimental GTK backend from PyGTK to PyGObject so there's an
   avenue forward for native Wayland support. (Must also add
   [gtk3-nocsd](https://github.com/PCMan/gtk3-nocsd) to the build so the Flatpak
   package knows how to obey when a non-GNOME desktop sets
   `LD_PRELOAD=libgtk3-nocsd.so.0` to prevent a usability regression.)

## How to Test Locally

1. Make sure you have [Flathub set up](https://flatpak.org/setup/) with suitably
   new versions of `flatpak` and `flatpak-builder` installed. (The flathub
   instructions should cover that too)
2. (Optional) Make sure you have the supporting validators installed locally:

   ```sh
   flatpak install flathub org.flathub.flatpak-external-data-checker org.freedesktop.appstream-glib
   ```

   (Note that the version of `appstream-util` from your distro package manager
   is likely to be an old version that is no longer aligned with current
   standards for good Appstream XML and may reject valid constructs.)

3. Run the following commands from the root of the repository:

   ```sh
   # -- Optional --
   flatpak run org.freedesktop.appstream-glib validate io.sourceforge.pysolfc.PySolFC.appdata.xml
   flatpak run org.flathub.flatpak-external-data-checker io.sourceforge.pysolfc.PySolFC.json
   # -- Required --
   flatpak-builder --user --install --force-clean build io.sourceforge.pysolfc.PySolFC.json
   flatpak run io.sourceforge.pysolfc.PySolFC
   ```

   (If flatpak complains about a missing version of `org.freedesktop.Sdk`, just
   `flatpak install` what it complained about and try again.)

While you're at it, you can also check something else that Flathub wants which
is outside the scope of this set of files by installing `desktop-file-utils`
with your system package manager and running `desktop-file-validate` on the
`.desktop` file. (As of this writing, it raises no issues.)

`flatpak-external-data-checker` will be run periodically for you by Flathub, but
you may want to setup GitHub Actions to verify that commits to your upstream
repo haven't broken any `.desktop` or `.appdata.xml` files you store in there,
since Flathub does want them to be correct but they're not Flatpak-specific.
