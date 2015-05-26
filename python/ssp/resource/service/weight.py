from resource.models import Domain, VieWeight

def zone_chengshi(file):
    zone_dict = {}
    for line in open(file).read().strip().split("\n"):
        if line.strip():
            key = line.strip().split("=")[0]
            value = [i for i in line.strip().split("=")[1].split(";")]
            zone_dict[key] = value
    return zone_dict

def get_chengshi_weight(view):
    view_list = view.strip().split("-")
    chsh = view_list[2]
    isp = view_list[3]
    chsh_weight = VieWeight.objects.get(view=chsh).weight
    isp_weight = VieWeight.objects.get(view=isp).weight
    view_chengshi_weight = chsh_weight * isp_weight
    return view_chengshi_weight

def get_zone_weight(view):
    view_list = view.strip().split("-")
    zone = view_list[3]
    isp = view_list[2]
    isp_weight = VieWeight.objects.get(view=isp).weight
    zone_dict = zone_chengshi("resource/service/domain_config")
    zone_weight = 0
    for item in zone_dict.get(zone):
        zone_weight += VieWeight.objects.get(view=item).weight
    view_zone_weight = zone_weight * isp_weight
    return view_zone_weight

def get_other_weight(view):
    isp_oj = VieWeight.objects.filter(typ='isp')
    isp_weight = sum([i['weight'] for i in isp_oj.values()])/isp_oj.count()
    view_list = view.split("-")
    if len(view_list) == 3:
        other_weight = VieWeight.objects.get(view=view_list[1]).weight        
    else:
        if view_list[1] == "China":
            other_weight = VieWeight.objects.get(view=view_list[2]).weight
        else:
            other_weight = VieWeight.objects.get(view=view_list[1]).weight
    view_other_weight = other_weight * isp_weight
    return view_other_weight

def get_weight(view):
    #print view
    vl = view.strip().split("-")
    if len(vl) >= 5:
        #print vl
        if "China" in vl[2] or vl[3] == "all":
            vw = get_zone_weight(view)
        else:
            vw = get_chengshi_weight(view)
    else:
        vw = get_other_weight(view)
    return vw