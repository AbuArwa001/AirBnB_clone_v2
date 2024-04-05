# Define variables in Puppet
$directory_name = '/data'
$web_static = "${directory_name}/web_static"
$releases = "${web_static}/releases"
$shared = "${web_static}/shared"
$test = "${releases}/test"
$fake_file = "${test}/index.html"
$link_name = "${web_static}/current"
$target_folder = $test
$nginx_conf = '/etc/nginx/sites-available/default'
$hbnb_static_config = "\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"

# Ensure Nginx is installed and running
package { 'nginx':
  ensure => installed,
  before => File[$nginx_conf],
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File[$nginx_conf],
}

# Create required directories
File {
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { [$directory_name, $web_static, $releases, $shared, $test]:
  ensure => directory,
  mode   => '0755',
}

# Create a fake index.html file
file { $fake_file:
  ensure  => file,
  content => 'Hello World',
  mode    => '0644',
}

# Ensure the symbolic link exists
file { $link_name:
  ensure => link,
  target => $target_folder,
  require => File[$fake_file],
}

# Backup the original Nginx config and update it
file { $nginx_conf:
  ensure  => file,
  content => template('path/to/your/template.erb'),
  backup  => '.backup.%F-%H-%M-%S',
  notify  => Service['nginx'],
}
