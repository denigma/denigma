# Patch generation methods, only available if the google-diff-match-patch
# library is installed.
#
# http://code.google.com/p/google-diff-match-patch/


try:
    from diff.diff_match_patch import diff_match_patch
except ImportError:
    pass
else:
    dmp = diff_match_patch()

    def generate_diffs(old_version, new_version, field_name, cleanup):
        """Generates a diff array for the named field between the two versions."""
        # Extract the text from the versions.
        old_text = old_version.field_dict[field_name] or u""
        new_text = new_version.field_dict[field_name] or u""
        # Generate the patch.
        diffs = dmp.diff_main(unicode(old_text), unicode(new_text))
        if cleanup == "semantic":
            dmp.diff_cleanupSemantic(diffs)
        elif cleanup == "efficiency":
            dmp.diff_cleanupEfficiency(diffs)
        elif cleanup is None:
            pass
        else:
            raise ValueError("cleanup parameter should be one of 'semantic', 'efficiency' or None.")
        return diffs

    def generate_patch(old_version, new_version, field_name, cleanup=None):
        """
        Generates a text patch of the named field between the two versions.
        
        The cleanup parameter can be None, "semantic" or "efficiency" to clean up the diff
        for greater human readibility.
        """
        diffs = generate_diffs(old_version, new_version, field_name, cleanup)
        patch = dmp.patch_make(diffs)
        return dmp.patch_toText(patch)

    def generate_patch_html(old_version, new_version, field_name, cleanup=None):
        """
        Generates a pretty html version of the differences between the named 
        field in two versions.
        
        The cleanup parameter can be None, "semantic" or "efficiency" to clean up the diff
        for greater human readibility.
        """
        diffs = generate_diffs(old_version, new_version, field_name, cleanup)
        return dmp.diff_prettyHtml(diffs)
