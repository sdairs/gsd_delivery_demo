<script lang="ts">
	import {} from 'carbon-components-svelte';

	export let order_data: object;
</script>

<table class="order-table">
	<tbody>
		<tr>
			<td>Order ID</td>
			<td>{order_data['order_id']}</td>
		</tr>
		<tr>
			<td>Customer Name</td>
			<td>{order_data['customer_name']}</td>
		</tr>
		<tr>
			<td>Destination Coords</td>
			<td>{order_data['destination_coords']}</td>
		</tr>
		<tr>
			<td>Destination Location</td>
			<td>{order_data['destination_location']}</td>
		</tr>
		<tr>
			<td>Pickup Coords</td>
			<td>{order_data['pickup_coords']}</td>
		</tr>
		<tr>
			<td>Pickup Location</td>
			<td>{order_data['pickup_location']}</td>
		</tr>
	</tbody>
</table>

<style>
	.order-table {
		border-collapse: collapse;
		margin: 25px 0;
		font-size: 0.9em;
		font-family: sans-serif;
		min-width: 400px;
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
	}
	.order-table thead tr {
		background-color: #009879;
		color: #ffffff;
		text-align: left;
	}
	.order-table th,
	.order-table td {
		padding: 12px 15px;
	}
	.order-table tbody tr {
		border-bottom: 1px solid #383838;
	}

	.order-table tbody tr:nth-of-type(even) {
		background-color: #252525;
	}

	.order-table tbody tr:last-of-type {
		border-bottom: 2px solid #009879;
	}
</style>
