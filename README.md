## i2DHT-ref

Implementation of P2P bootstraping and networking using Kademlia like DHT. 
Please Note! this is just the reference implementation.

## Usage

```
python setup.py develop

usage: i2dht [-h] [-p PORT] [-b BOOTSTRAP] [-f FIND]

Bootstrap demo for P2P kademlia dht

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port
  -b BOOTSTRAP, --bootstrap BOOTSTRAP
                        Bootstrap nodes
  -f FIND, --find FIND  Find node id

## example

4322382356302711371578667
127.0.0.1 53000
Starting the DHTServer .....
902611019455853395359454395902312787167616363795  -----------> RPCID

i2dht --port 55000
i2dht --port 54000 --bootstrap 1234617559663651537718677970167272701639314515907:127.0.0.1:55000
i2dht --port 53000 --bootstrap 440506452073837681358424322382356302711371578667:127.0.0.1:54000
i2dht --port 52000 --bootstrap 476399684551155124839879384859492889739957742343:127.0.0.1:53000 --find 440506452073837681358424322382356302711371578667

```

NOTE: Its is just the reference implementation.

