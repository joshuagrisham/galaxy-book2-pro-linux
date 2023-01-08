modprobe pci-stub
modprobe vfio-pci

echo 0000:00:1f.X | sudo tee /sys/bus/pci/devices/0000:00:1f.X/driver/unbind <- for X in {0, 3, 4, 5}
echo 0x8086 0xWXYZ | sudo tee /sys/bus/pci/drivers/vfio-pci/new_id <- for WXYZ in {5182, 51c8, 51a3, 51a4}

#for dev in "$@"; do
#        vendor=$(cat /sys/bus/pci/devices/$dev/vendor)
#        device=$(cat /sys/bus/pci/devices/$dev/device)
#        if [ -e /sys/bus/pci/devices/$dev/driver ]; then
#                echo $dev > /sys/bus/pci/devices/$dev/driver/unbind
#        fi
#        echo $vendor $device > /sys/bus/pci/drivers/vfio-pci/new_id
#done
