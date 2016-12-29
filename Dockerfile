
#--------------------------------
# Platform Requested
#--------------------------------

FROM ubuntu:16.04
MAINTAINER verticalduck@gmail.com

# Non-interactive install of ubuntu packages
ENV DEBIAN_FRONTEND noninteractive
ENV HOME_DIR /root
ENV APP_NAME mantaflow

#--------------------------------
# Install packages
#--------------------------------

RUN apt-get update -y \
    && apt-get -y install \
      g++ \
      git \
      cmake \
      python \
      make \
      libtbb-dev \
      python-dev

#--------------------------------
# Copy stuff
#--------------------------------

COPY . /root/manta
WORKDIR /root/manta

#--------------------------------
# BUILD manta
#--------------------------------

# compiling arcsim
RUN mkdir -p build2 bin \
    && cd build2 \
    && cmake -DDEBUG=OFF -DGUI=OFF -DTBB=ON .. \
    && make -j4 VERBOSE=1 \
    && cp manta /usr/local/bin/ \
    && cd .. \
    && rm -rf build2
        
ENV DEBIAN_FRONTEND newt
