<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="<?php print $language ?>" xml:lang="<?php print $language ?>">

<head>
  <title><?php print $head_title ?></title>
  <?php print $head ?>
  <?php print $styles ?>
  <script type="text/javascript"><?php /* Needed to avoid Flash of Unstyle Content in IE */ ?> </script>
</head>

<body>
<div id="page_wrapper">
  <div id="header_wrapper">
    <div id="header">
      <?php /*<h1>News<font color="#FFDF8C">Portal</font></h1>*/ ?>
      <?php if ($site_name) { ?><h1><a href="<?php print $base_path ?>" id="sitename" title="<?php print t('Home') ?>"><?php print $site_name ?></a></h1><?php } ?>
      <?php if ($site_slogan) { ?><h2><?php print $site_slogan ?></h2><?php } ?>
    </div>
    <div id="navcontainer">
      <?php if (isset($primary_links)) { ?><?php print newsportal_primary_links() ?><?php } ?>
    </div>
  </div>
  <?php if ($sidebar_left) { ?><div id="left_side">
      <?php print $sidebar_left ?>
  </div><?php } ?>

  <?php if ($sidebar_right) { ?><div id="right_side">
      <?php print $sidebar_right ?>
  </div><?php } ?>

  <div id="content">
    <div><?php print $header ?></div>
    <?php if ($mission) { ?><div class="featurebox_center"><?php print $mission ?></div><?php } ?>
    <?php print $breadcrumb ?>
    <h3><?php print $title ?></h3>
    <div class="tabs"><?php print $tabs ?></div>
    <?php print $help ?>
    <?php print $messages ?>
    <?php print $content; ?>
  </div>

  <div id="footer">
    <?php if (isset($secondary_links)) { ?><?php print newsportal_secondary_links() ?><br /><?php } ?>
    <?php print $footer_message ?>
  </div>

</div>
<?php print $closure ?>
</body>
</html>
