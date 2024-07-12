<?php
$apiKey = "rzp_live_yvVm7djbY9U18g";
?>
<form action="" method="POST">
<script
    src="https://checkout.razorpay.com/v1/checkout.js"
    data-key="<?php echo $apikey; ?>"
    data-amount="<?php echo $_POST['amount']*100;?>"
    data-currency="INR"
    data-id="<?php echo 'OID'.rand(10,100).'END';?>"
    data-buttontext="Pay with Razorpay"
    data-name="Urban Ninja"
    data-description="A mini project to integrate payment gateway also in website"
    data-prefill.name="<?php echo $_POST['name'];?>"
    data-prefill.email="<?php echo $_POST['email'];?>"
    data-theme.color="#F37254"
></script>
<input type="hidden" custom="Hidden Element" name="hidden"/>
</form>