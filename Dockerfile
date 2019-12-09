FROM python:3.7-alpine

RUN pip install requests argparse mysql-connector beautifulsoup4 isodate schedule
COPY . /usr/src/themoviepredictor
CMD python /usr/src/themoviepredictor/app5_apirest.py movies list

WORKDIR /usr/src/themoviepredictor

#  COLOR_NC='\e[0m' # No Color
#  COLOR_WHITE='\e[1;37m'
#  COLOR_BLACK='\e[0;30m'
#  COLOR_BLUE='\e[0;34m'
#  COLOR_LIGHT_BLUE='\e[1;34m'
#  COLOR_GREEN='\e[0;32m'
#  COLOR_LIGHT_GREEN='\e[1;32m'
#  COLOR_CYAN='\e[0;36m'
#  COLOR_LIGHT_CYAN='\e[1;36m'
#  COLOR_RED='\e[0;31m'
#  COLOR_LIGHT_RED='\e[1;31m'
#  COLOR_PURPLE='\e[0;35m'
#  COLOR_LIGHT_PURPLE='\e[1;35m'
#  COLOR_BROWN='\e[0;33m'
#  COLOR_YELLOW='\e[1;33m'
#  COLOR_GRAY='\e[0;30m'
#  COLOR_LIGHT_GRAY='\e[0;37m'

ENV PS1="\n\e[1;34m\w\e[0;37m\$ "


# RUN apt-get install -y locales
# RUN echo 'fr_FR.UTF-8 UTF-8' >> /etc/locale.gen 
# RUN echo 'fr_FR ISO-8859-1' >> /etc/locale.gen
# RUN locale-gen

# ou US:

# RUN echo 'en_US ISO-8859-1 ' >> /etc/locale.gen 
# RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen 