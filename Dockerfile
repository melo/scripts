FROM melopt/perl-alt:perl-latest-build AS build

COPY cpanfile /app
RUN cd /app && pdi-build-deps


FROM melopt/perl-alt:perl-latest-devel

ENV PATH=/tools/bin:/deps/bin:/deps/local/bin:/stack/bin:/stack/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY --from=build /deps /deps
COPY bin/ /tools/bin/
