<script lang="ts">
import { Button } from "carbon-components-svelte";

	export let order_history: Array<object>;
</script>

<table class="order-table">
	<tbody>
		{#each order_history as order}
			<tr>
				<td>{order['order_id']}</td>
				<td>{order['customer_name']}</td>
				<td>{order['destination_location']}</td>
				<td>{order['pickup_location']}</td>
				<td>{order['time_ordered']}</td>
				<Button on:click data-order-id={order['order_id']}>Search</Button>
			</tr>
		{/each}
	</tbody>
</table>

<style>
	.order-table {
		display: block;
		border-collapse: collapse;
		font-size: 0.9em;
		font-family: sans-serif;
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
		width: 100%;
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
