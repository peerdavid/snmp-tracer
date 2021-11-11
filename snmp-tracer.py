# See also


from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp, udp6
from pysnmp.entity.rfc3413 import ntfrcv
# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()
# Execution point observer setup
# Register a callback to be invoked at specified execution point of
# SNMP Engine and passed local variables at code point's local scope
# noinspection PyUnusedLocal,PyUnusedLocal
def requestObserver(snmpEngine, execpoint, variables, cbCtx):
    print('Execution point: %s' % execpoint)
    print('* transportDomain: %s' % '.'.join([str(x) for x in variables['transportDomain']]))
    print('* transportAddress: %s' % '@'.join([str(x) for x in variables['transportAddress']]))
    print('* securityModel: %s' % variables['securityModel'])
    print('* securityName: %s' % variables['securityName'])
    print('* secuhttps://man.archlinux.org/man/community/python-pysnmp/pysnmp.1.enrityLevel: %s' % variables['securityLevel'])
    print('* contextEngineId: %s' % variables['contextEngineId'].prettyPrint())
    print('* contextName: %s' % variables['contextName'].prettyPrint())
    print('* PDU: %s' % variables['pdu'].prettyPrint())
snmpEngine.observer.registerObserver(
    requestObserver,
    'rfc3412.receiveMessage:request',
    'rfc3412.returnResponsePdu'
)
# Transport setup
# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('127.0.0.1', 162))
)
# UDP over IPv6
config.addTransport(
    snmpEngine,
    udp6.domainName,
    udp6.Udp6Transport().openServerMode(('::1', 162))
)
# SNMPv1/2c setup
# SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')
# Callback function for receiving notifications
# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print('Notification from ContextEngineId "%s", ContextName "%s"' % (contextEngineId.prettyPrint(),
                                                                        contextName.prettyPrint()))
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)
snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish
# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.observer.unregisterObserver()
    snmpEngine.transportDispatcher.closeDispatcher()
    raise