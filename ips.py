import iptools

def get_ips(cidr):

    # new_ips = []
    # new_ip = None
    # for ip in iptools.IpRange(cidr):
	   #  new_ips.append(ip)


    return [ip for ip in iptools.IpRange(cidr)]