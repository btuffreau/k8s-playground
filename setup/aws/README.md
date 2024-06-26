# Setup

- pre provisioned minimalistic VPC with one AZ in a public subnet
- allowed ssh inbound in default SG
- created keypair `interview` and stored in ASM

```bash
NAME="johndoe"
./setup.sh $NAME
```

The setup will take a couple of minutes after the instance is running, you can follow progress like so:

```bash
ssh -i $HOME/interview-rsa.pem ${instance-dns} # Use output from setup.sh
tail -f /var/log/cloud-init-output.log
```

```bash
#Candidate
ssh-keygen -f $HOME/.ssh/interview -t rsa -b 4096 -N '' <<<$'\n'
cat $HOME/.ssh/interview.pub # needs to be copied over to the instance
```

```bash
# candidate_pkey is the public key file received from the candidate
ssh-copy-id -o "IdentityFile=$HOME/interview-rsa.pem" -i {candidate_pkey} \
  ec2-user@ec2-.....compute.amazonaws.com
```

To copy an additional public key to the instance:

```bash
candidatePublicKeyPath=<<PUBLICKEY>> # Path to pkey file: /tmp/johndoe.pub
instanceDns="<<EC2_PUBLIC_DNS_NAME>>"
cat ${candidatePublicKeyPath} | ssh -i $HOME/interview-rsa.pem ${instanceDns} "cat >> ~/.ssh/authorized_keys"
```

**Kill the instance when done!**