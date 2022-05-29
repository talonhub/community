
  { config, pkgs, lib, ... }:
  
  let
    user = "pi";
    password = "pi";
    SSID = "CasaDelMaciek";
    SSIDpassword = "un%^3ro*^TjF9GubquXfc%&KeserXyLpufL3G&T9YDTPWJAkf!DbPKehY$e6";
    interface = "wlan0";
    hostname = "raspberrypi01";
  in {
    imports = ["${fetchTarball "https://github.com/NixOS/nixos-hardware/archive/936e4649098d6a5e0762058cb7687be1b2d90550.tar.gz" }/raspberry-pi/4"];

    fileSystems = {
      "/" = {
        device = "/dev/disk/by-label/NIXOS_SD";
        fsType = "ext4";
        options = [ "noatime" ];
      };
    };

    networking = {
      hostName = hostname;
      
      wireless = {
        enable = true;
        networks."${SSID}".psk = SSIDpassword;
        interfaces = [ interface ];
      };
    };

    environment.systemPackages = with pkgs; [ vim ];

    services.openssh = {
enable = true;
passwordAuthentication = false;
 permitRootLogin = "no";
};

    users = {
      mutableUsers = false;
      users."${user}" = {
        isNormalUser = true;
        password = password;
        extraGroups = [ "wheel" "docker" ];
	openssh.authorizedKeys.keys = ["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFStShWQ39dkULs/sI8YElj/U6gRfZgfQ4Ef+ce0kilA maciej.klimek@gmail.com"];
      };
    };

    # Enable GPU acceleration
    hardware.raspberry-pi."4".fkms-3d.enable = true;

    services.xserver = {
      enable = true;
      displayManager.lightdm.enable = true;
      desktopManager.xfce.enable = true;
    };
    

    hardware.pulseaudio.enable = true;
 virtualisation.docker.enable = true;
    
  }