<?php
// $Id: template.php,v 1.2 2006/08/20 05:59:21 Gurpartap Exp $

function newsportal_primary_links() {
  $links = menu_primary_links();
  if ($links) {
    $output .= '<ul id="navlist">';
    foreach ($links as $link) {

      $output .= '<li>' . $link . '</li>';
    }; 
    $output .= '</ul>';
  }
  return $output;
}

function newsportal_secondary_links() {
  $links = menu_secondary_links();
  if ($links) {
  $output = implode("&nbsp;|&nbsp;",$links);
  }
  return $output;
}

function _phptemplate_variables($hook, $vars = array()) {
  switch ($hook) {
    case 'page':
      if (arg(0) == 'portal') {
        $vars['template_file'] = 'page-portal';
      }
      break;
  }

  return $vars;
}

