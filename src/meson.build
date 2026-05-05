pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'openrtel'
gnome = import('gnome')

gnome.compile_resources('openrtel',
  'openrtel.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

sdr_dep = dependency('rtlsdr')



conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'openrtel.in',
  output: 'openrtel',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

openrtel_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'controls.py'
]

install_data(openrtel_sources, install_dir: moduledir)
