#sudo ./vfio-bind.sh 0000\:00\:1f.0
#sudo ./vfio-bind.sh 0000\:00\:1f.3
#sudo ./vfio-bind.sh 0000\:00\:1f.4
#sudo ./vfio-bind.sh 0000\:00\:1f.5

sudo ./qemu-system-x86_64 -enable-kvm -hda win10.img -m 8G -cpu host,kvm=off \
 -device vfio-pci,host=0000:00:1f.0,multifunction=on,x-no-mmap=true \
 -device vfio-pci,host=0000:00:1f.3,multifunction=on,x-no-mmap=true \
 -device vfio-pci,host=0000:00:1f.4,multifunction=on,x-no-mmap=true \
 -device vfio-pci,host=0000:00:1f.5,multifunction=on,x-no-mmap=true \
 -trace events=./startvm-events.txt -monitor stdio \
 -L /home/joshua/windows_vm/qemu/build/pc-bios/
