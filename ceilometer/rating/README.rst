Steps to add plugin into ceilometer

1. entry points (ex: /usr/lib/python2.7/dist-packages/ceilometer-2015.1.2.egg-info/entry_points.txt)
insert into section [ceilometer.poll.central]  
cloudkitty.rating = ceilometer.rating.cloudkitty:RatingCostPollster

2. adjust /etc/ceilometer/pipeline.yaml
sources:
    ...
    - name: rating_source
      interval: 1800
      meters:
          - "cloudkitty.rating"
      sinks:
          - rating_sink
sinks:
    ...
    - name: rating_sink
      transformers:
      publishers:
          - notifier://
