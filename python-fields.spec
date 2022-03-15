#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Container class boilerplate killer
Summary(pl.UTF-8):	Zabójca ramowego kodu klas kontenerów
Name:		python-fields
Version:	5.0.0
Release:	4
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/fields/
Source0:	https://files.pythonhosted.org/packages/source/f/fields/fields-%{version}.tar.gz
# Source0-md5:	4b3a60ddaad146f698979cf4da2639d4
Patch0:		%{name}-docs.patch
Patch1:		%{name}-tests.patch
URL:		https://github.com/ionelmc/python-fields
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-characteristic
BuildRequires:	python-pytest
BuildRequires:	python-pytest-benchmark
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-characteristic
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-benchmark
%endif
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_py3doc_enhanced_theme
# with sphinx.ext.napoleon
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Container class boilerplate killer. Features:
- Human-readable __repr__
- Complete set of comparison methods
- Keyword and positional argument support. Works like a normal class -
  you can override just about anything in the subclass (eg: a custom
  __init__).

%description -l pl.UTF-8
Zabójca ramowego kodu klas kontenerów. Możliwości:
- __repr__ czytelne dla człowieka
- pełny zbiór metod porównujących
- obsługa argumentów pozycyjnych i słownikowych; działa jak zwykła
  klasa - można przeciążać prawie wszystko w podklasie (np. własny
  __init__).

%package -n python3-fields
Summary:	Container class boilerplate killer
Summary(pl.UTF-8):	Zabójca ramowego kodu klas kontenerów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-fields
Container class boilerplate killer. Features:
- Human-readable __repr__
- Complete set of comparison methods
- Keyword and positional argument support. Works like a normal class -
  you can override just about anything in the subclass (eg: a custom
  __init__).

%description -n python3-fields -l pl.UTF-8
Zabójca ramowego kodu klas kontenerów. Możliwości:
- __repr__ czytelne dla człowieka
- pełny zbiór metod porównujących
- obsługa argumentów pozycyjnych i słownikowych; działa jak zwykła
  klasa - można przeciążać prawie wszystko w podklasie (np. własny
  __init__).

%package apidocs
Summary:	API documentation for Python fields module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona fields
Group:		Documentation

%description apidocs
API documentation for Python fields module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona fields.

%prep
%setup -q -n fields-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_benchmark.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_benchmark.plugin" \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
cd docs
PYTHONPATH=$(pwd)/../src \
sphinx-build-3 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/fields
%{py_sitescriptdir}/fields-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-fields
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/fields
%{py3_sitescriptdir}/fields-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,*.html,*.js}
%endif
